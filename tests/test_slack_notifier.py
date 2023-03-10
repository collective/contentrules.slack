from . import HTTPXMock
from contentrules.slack import settings
from contentrules.slack.interfaces import ISlackNotifier
from contentrules.slack.slack_notifier import NOTIFICATION_DEACTIVATION_VALUE
from contentrules.slack.slack_notifier import notify_slack
from contentrules.slack.slack_notifier import SlackNotifier
from zope.component import getUtility
from zope.interface.verify import verifyClass


class TestNotifier:
    def test_implements_interface(self):
        assert verifyClass(ISlackNotifier, SlackNotifier) is True

    def test_utility_is_registered_properly(self):
        slack_notifier = getUtility(ISlackNotifier)
        assert isinstance(slack_notifier, SlackNotifier) is True

    def test_notify_to_webhook_performs_a_post_request(self, wait_for):
        with HTTPXMock.installed() as requests:
            wait_for(notify_slack("https://hooks.slack.com/services/foo"))
            assert len(requests.posts) == 1
            assert (
                requests.posts[0].get("url") == "https://hooks.slack.com/services/foo"
            )

    def test_notify_includes_request_payload(self, wait_for):
        with HTTPXMock.installed() as requests:
            wait_for(
                notify_slack("https://hooks.slack.com/services/foo", text="Foo bar")
            )

            assert len(requests.posts) == 1
            assert (
                requests.posts[0].get("url") == "https://hooks.slack.com/services/foo"
            )
            assert requests.posts[0].get("json") == {"text": "Foo bar"}

    def test_notify_to_webhook_without_webhook_url_will_use_standard_slack_webhook_url(
        self, monkeypatch, portal, wait_for
    ):
        monkeypatch.setattr(
            settings, "SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/bar"
        )
        with HTTPXMock.installed() as requests:
            wait_for(notify_slack())
            assert (
                requests.posts[0].get("url") == "https://hooks.slack.com/services/bar"
            )

    def test_do_not_post_if_no_webhook_url_is_available(
        self, monkeypatch, portal, wait_for
    ):
        monkeypatch.setattr(settings, "SLACK_WEBHOOK_URL", "")
        with HTTPXMock.installed() as requests:
            wait_for(notify_slack())
            assert len(requests.posts) == 0

    def test_do_not_post_if_webhook_contains_notification_deactivation_value(
        self, portal, wait_for
    ):
        with HTTPXMock.installed() as requests:
            wait_for(notify_slack(NOTIFICATION_DEACTIVATION_VALUE))
            assert len(requests.posts) == 0

    def test_do_not_perform_a_request_if_slacker_is_globally_deactivated(
        self, monkeypatch, portal, wait_for
    ):
        monkeypatch.setattr(
            settings, "DEACTIVATE_SLACK_NOTIFICATION", NOTIFICATION_DEACTIVATION_VALUE
        )
        with HTTPXMock.installed() as requests:
            wait_for(notify_slack("https://hooks.slack.com/services/foo"))
            assert len(requests.posts) == 0

    def test_default_request_parameters(self, wait_for):
        with HTTPXMock.installed() as requests:
            wait_for(notify_slack("https://hooks.slack.com/services/foo"))
            assert requests.posts[0]["json"] == {}
            assert requests.posts[0]["timeout"] == 2
            assert requests.posts[0]["url"] == "https://hooks.slack.com/services/foo"
            assert requests.posts[0]["verify"] is True

    def test_override_default_request_parameters_is_possible(self, wait_for):
        with HTTPXMock.installed() as requests:
            wait_for(
                notify_slack(
                    "http://someurl",
                    timeout=5,
                    verify=False,
                    param1="Foo",
                    param2="Bar",
                )
            )
            assert requests.posts[0]["json"] == {"param1": "Foo", "param2": "Bar"}
            assert requests.posts[0]["timeout"] == 5
            assert requests.posts[0]["url"] == "http://someurl"
            assert requests.posts[0]["verify"] is False
