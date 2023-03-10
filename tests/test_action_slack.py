from . import HTTPXMock
from contentrules.slack.actions.slack import SlackAction
from contentrules.slack.actions.slack import SlackAddFormView
from contentrules.slack.actions.slack import SlackEditFormView
from plone.app.contentrules.rule import Rule
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface.interfaces import IObjectEvent

import pytest


@pytest.fixture
def payload() -> dict:
    return {
        "webhook_url": "https://hooks.slack.com/services/T00000000/B00000000/YYYYYYYYYYYYYYYYYYYYYYYY",  # noqa
        "channel": "#tests",
        "pretext": "What about this new document?",
        "title": "Document with title ${title}",
        "title_link": "${absolute_url}",
        "text": "Hello word! ${review_state_title}",
        "color": "danger",
        "icon": ":flag-br:",
        "username": "Plone Buttler",
        "fields": "Title|${title}|True\nReview State|${review_state_title}|True",
    }


@pytest.fixture
def slack_action(payload) -> SlackAction:
    e = SlackAction()
    for attr, value in payload.items():
        setattr(e, attr, value)
    return e


@implementer(IObjectEvent)
class DummyEvent:
    def __init__(self, object):
        self.object = object


class TestAction:
    def test_registered(self):
        element = getUtility(IRuleAction, name="plone.actions.Slack")
        assert "plone.actions.Slack" == element.addview
        assert "edit" == element.editview
        assert element.for_ is None

    def test_invoke_add_View(self, portal, payload, http_request):
        element = getUtility(IRuleAction, name="plone.actions.Slack")
        storage = getUtility(IRuleStorage)
        storage["foo"] = Rule()
        rule = portal.restrictedTraverse("++rule++foo")
        adding = getMultiAdapter((rule, http_request), name="+action")
        addview = getMultiAdapter((adding, http_request), name=element.addview)
        assert isinstance(addview, SlackAddFormView) is True

        addview.form_instance.update()
        output = addview.form_instance()
        assert "<h2>Substitutions</h2>" in output

        content = addview.form_instance.create(data=payload)
        addview.form_instance.add(content)
        e = rule.actions[0]
        assert isinstance(e, SlackAction) is True
        assert e.summary.startswith("Post a message on channel")
        assert "https://hooks.slack.com/" in e.webhook_url
        assert "#tests" == e.channel
        assert payload["title"] == e.title
        assert payload["title_link"] == e.title_link
        assert payload["pretext"] == e.pretext
        assert payload["text"] == e.text
        assert payload["color"] == e.color
        assert payload["icon"] == e.icon
        assert payload["username"] == e.username
        assert payload["fields"] == e.fields

    def test_invoke_edit_view(self, http_request):
        element = getUtility(IRuleAction, name="plone.actions.Slack")
        e = SlackAction()
        editview = getMultiAdapter((e, http_request), name=element.editview)
        assert isinstance(editview, SlackEditFormView) is True

    def test_payload(self, slack_action, folder, doc):
        ex = getMultiAdapter((folder, slack_action, DummyEvent(doc)), IExecutable)
        payload = ex.get_message_payload()
        assert "Hello word! Private" == payload["text"]

        attachment = payload["attachments"][0]
        fields = attachment["fields"]
        assert "Document with title A Document" == attachment["title"]
        assert len(fields) == 2
        assert fields[0]["value"] == "A Document"

    def test_payload_with_none_values(self, slack_action, folder, doc):
        slack_action.title = None
        slack_action.pretext = None
        ex = getMultiAdapter((folder, slack_action, DummyEvent(doc)), IExecutable)
        payload = ex.get_message_payload()

        attachment = payload["attachments"][0]
        fields = attachment["fields"]
        assert attachment["title"] == ""
        assert len(fields) == 2
        assert fields[0]["value"] == "A Document"

    def test_execute(self, slack_action, wait_for, folder, doc):
        ex = getMultiAdapter((folder, slack_action, DummyEvent(doc)), IExecutable)
        with HTTPXMock.installed() as requests:
            payload = ex.get_payload()
            wait_for(ex.notify_slack(payload))
            assert len(requests.posts) == 1
            post = requests.posts[0]
            assert post.get("url") == payload["webhook_url"]
            assert post.get("timeout") == 10
            assert post.get("verify") is True
            assert "text" in post.get("json")
            assert "attachments" in post.get("json")
