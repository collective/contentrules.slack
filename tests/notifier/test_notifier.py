"""Posting to Slack, and the two ways of switching it off."""

from contentrules.slack import settings
from contentrules.slack.interfaces import ISlackNotifier
from contentrules.slack.slack_notifier import NOTIFICATION_DEACTIVATION_VALUE
from contentrules.slack.slack_notifier import notify_slack
from contentrules.slack.slack_notifier import SlackNotifier
from zope.component import getUtility
from zope.interface.verify import verifyClass

import pytest
import requests


WEBHOOK_URL = "https://hooks.slack.com/services/foo"


class TestNotifierRegistration:
    def test_implements_interface(self):
        assert verifyClass(ISlackNotifier, SlackNotifier) is True

    def test_utility_is_registered(self, portal):
        assert isinstance(getUtility(ISlackNotifier), SlackNotifier)


@pytest.mark.usefixtures("portal")
class TestNotify:
    def test_posts_to_the_webhook(self, mock_requests, wait_for):
        wait_for(notify_slack(WEBHOOK_URL))
        assert len(mock_requests.posts) == 1
        assert mock_requests.posts[0]["url"] == WEBHOOK_URL

    def test_runs_in_a_named_thread(self, mock_requests, wait_for):
        thread = notify_slack(WEBHOOK_URL)
        wait_for(thread)
        assert thread is not None
        assert thread.name == SlackNotifier.THREAD_NAME

    def test_payload_is_sent_as_json(self, mock_requests, wait_for):
        wait_for(notify_slack(WEBHOOK_URL, text="Foo bar"))
        assert mock_requests.posts[0]["json"] == {"text": "Foo bar"}

    def test_default_request_parameters(self, mock_requests, wait_for):
        wait_for(notify_slack(WEBHOOK_URL))
        post = mock_requests.posts[0]
        assert post["json"] == {}
        assert post["timeout"] == 2
        assert post["verify"] is True

    def test_override_request_parameters(self, mock_requests, wait_for):
        wait_for(
            notify_slack(
                "http://someurl",
                timeout=5,
                verify=False,
                param1="Foo",
                param2="Bar",
            )
        )
        post = mock_requests.posts[0]
        assert post["json"] == {"param1": "Foo", "param2": "Bar"}
        assert post["timeout"] == 5
        assert post["url"] == "http://someurl"
        assert post["verify"] is False

    def test_falls_back_to_the_webhook_setting(
        self, monkeypatch, mock_requests, wait_for
    ):
        monkeypatch.setattr(settings, "SLACK_WEBHOOK_URL", WEBHOOK_URL)
        wait_for(notify_slack())
        assert mock_requests.posts[0]["url"] == WEBHOOK_URL

    def test_the_webhook_passed_wins_over_the_setting(
        self, monkeypatch, mock_requests, wait_for
    ):
        monkeypatch.setattr(settings, "SLACK_WEBHOOK_URL", "https://other")
        wait_for(notify_slack(WEBHOOK_URL))
        assert mock_requests.posts[0]["url"] == WEBHOOK_URL


@pytest.mark.usefixtures("portal")
class TestNotifyDeactivated:
    def test_no_webhook_available(self, monkeypatch, mock_requests, wait_for):
        monkeypatch.setattr(settings, "SLACK_WEBHOOK_URL", "")
        thread = notify_slack()
        wait_for(thread)
        assert thread is None
        assert mock_requests.posts == []

    @pytest.mark.parametrize(
        "webhook_url",
        [
            NOTIFICATION_DEACTIVATION_VALUE,
            NOTIFICATION_DEACTIVATION_VALUE.upper(),
        ],
    )
    def test_webhook_is_the_deactivation_value(
        self, mock_requests, wait_for, webhook_url
    ):
        thread = notify_slack(webhook_url)
        wait_for(thread)
        assert thread is None
        assert mock_requests.posts == []

    def test_setting_is_the_deactivation_value(
        self, monkeypatch, mock_requests, wait_for
    ):
        monkeypatch.setattr(settings, "SLACK_WEBHOOK_URL", "deactivate")
        wait_for(notify_slack())
        assert mock_requests.posts == []

    @pytest.mark.parametrize(
        "value",
        [
            NOTIFICATION_DEACTIVATION_VALUE,
            NOTIFICATION_DEACTIVATION_VALUE.capitalize(),
        ],
    )
    def test_globally_deactivated(self, monkeypatch, mock_requests, wait_for, value):
        monkeypatch.setattr(settings, "DEACTIVATE_SLACK_NOTIFICATION", value)
        thread = notify_slack(WEBHOOK_URL)
        wait_for(thread)
        assert thread is None
        assert mock_requests.posts == []

    def test_other_values_do_not_deactivate(self, monkeypatch, mock_requests, wait_for):
        monkeypatch.setattr(settings, "DEACTIVATE_SLACK_NOTIFICATION", "no")
        wait_for(notify_slack(WEBHOOK_URL))
        assert len(mock_requests.posts) == 1


class TestDoRequest:
    """The request itself, run synchronously rather than in a thread."""

    def test_success(self, mock_requests):
        SlackNotifier()._do_request(WEBHOOK_URL, 2, True, text="Foo")
        assert mock_requests.posts == [
            {
                "url": WEBHOOK_URL,
                "timeout": 2,
                "verify": True,
                "json": {"text": "Foo"},
            }
        ]

    def test_error_status_raises(self, mock_requests):
        mock_requests.status_code = 404
        with pytest.raises(requests.HTTPError):
            SlackNotifier()._do_request(WEBHOOK_URL, 2, True, text="Foo")
