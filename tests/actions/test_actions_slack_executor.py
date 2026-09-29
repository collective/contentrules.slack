"""Building the Slack message for the object that triggered a rule."""

from contentrules.slack.actions.slack import safe_attr
from contentrules.slack.actions.slack import SlackAction
from contentrules.slack.actions.slack import SlackActionExecutor

import pytest


class TestSafeAttr:
    def test_value(self, slack_action):
        assert safe_attr(slack_action, "channel") == "#tests"

    def test_none_reads_as_empty(self, slack_action):
        slack_action.pretext = None
        assert safe_attr(slack_action, "pretext") == ""


class TestExecutor:
    def test_adapter(self, executor, slack_action):
        assert isinstance(executor(slack_action), SlackActionExecutor)

    def test_notifier_config(self, executor, slack_action, payload):
        assert executor(slack_action).get_notifier_config() == {
            "webhook_url": payload["webhook_url"],
            "timeout": 10,
            "verify": True,
        }

    def test_get_payload_combines_message_and_config(self, executor, slack_action):
        ex = executor(slack_action)
        result = ex.get_payload()
        assert result == {**ex.get_message_payload(), **ex.get_notifier_config()}


class TestMessagePayload:
    @pytest.fixture
    def message(self, executor, slack_action) -> dict:
        return executor(slack_action).get_message_payload()

    @pytest.fixture
    def attachment(self, message) -> dict:
        return message["attachments"][0]

    def test_single_attachment(self, message):
        assert len(message["attachments"]) == 1

    @pytest.mark.parametrize(
        "key,expected",
        [
            ["text", "Hello world! Private"],
            ["channel", "#tests"],
            ["username", "Plone Butler"],
            ["icon_emoji", ":flag-br:"],
        ],
    )
    def test_message(self, message, key, expected):
        assert message[key] == expected

    @pytest.mark.parametrize(
        "key,expected",
        [
            ["title", "Document with title A Document"],
            ["pretext", "What about this new document?"],
            ["fallback", "Hello world! Private"],
            ["color", "danger"],
        ],
    )
    def test_attachment(self, attachment, key, expected):
        assert attachment[key] == expected

    def test_title_link_is_interpolated(self, attachment, doc):
        assert attachment["title_link"] == doc.absolute_url()

    def test_fields(self, attachment):
        assert attachment["fields"] == [
            {"title": "Title", "value": "A Document", "short": True},
            {"title": "Review State", "value": "Private", "short": False},
        ]


class TestMessagePayloadEdgeCases:
    def test_none_values(self, executor, slack_action):
        """Optional settings left empty in the form are stored as None."""
        slack_action.title = None
        slack_action.pretext = None
        slack_action.color = None
        slack_action.fields = None
        attachment = executor(slack_action).get_message_payload()["attachments"][0]
        assert attachment["title"] == ""
        assert attachment["pretext"] == ""
        assert attachment["color"] == ""
        assert attachment["fields"] == []

    def test_values_are_stripped(self, executor, slack_action):
        slack_action.text = "  ${title}  "
        slack_action.fields = "Title| ${title} |true"
        message = executor(slack_action).get_message_payload()
        assert message["text"] == "A Document"
        assert message["attachments"][0]["fields"][0]["value"] == "A Document"

    def test_channel_is_not_interpolated(self, executor, slack_action):
        slack_action.channel = "#${id}"
        message = executor(slack_action).get_message_payload()
        assert message["channel"] == "#${id}"

    def test_defaults(self, executor):
        """An action created without settings still builds a message."""
        message = executor(SlackAction()).get_message_payload()
        assert message["text"] == ""
        assert message["attachments"][0]["fields"] == []


class TestNotify:
    def test_notify_slack(self, executor, slack_action, mock_requests, wait_for):
        ex = executor(slack_action)
        payload = ex.get_payload()
        wait_for(ex.notify_slack(payload))
        assert len(mock_requests.posts) == 1
        post = mock_requests.posts[0]
        assert post["url"] == payload["webhook_url"]
        assert post["timeout"] == 10
        assert post["verify"] is True
        assert post["json"] == ex.get_message_payload()

    def test_call(self, executor, slack_action, mock_requests, wait_for_notifications):
        assert executor(slack_action)() is True
        wait_for_notifications()
        assert len(mock_requests.posts) == 1
        assert mock_requests.posts[0]["json"]["channel"] == "#tests"
