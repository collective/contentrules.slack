from contentrules.slack.actions.slack import SlackAction
from contentrules.slack.actions.slack import SlackAddFormView
from contentrules.slack.actions.slack import SlackEditFormView
from contentrules.slack.testing import CONTENTRULES_SLACK_INTEGRATION_TESTING
from ftw.slacker.tests import RequestsMock
from plone import api
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.interfaces import IObjectEvent
from zope.interface import implementer

import unittest


ACTION_PAYLOAD = {
    "webhook_url": "https://hooks.slack.com/services/T00000000/B00000000/YYYYYYYYYYYYYYYYYYYYYYYY",
    "channel": u"#tests",
    "pretext": u"What about this new document?",
    "title": u"Document with title ${title}",
    "title_link": u"${absolute_url}",
    "text": u"Hello word! ${review_state_title}",
    "color": u"danger",
    "icon": u":flag-br:",
    "username": u"Plone Buttler",
    "fields": u"Title|${title}|True\nReview State|${review_state_title}|True",
}


@implementer(IObjectEvent)
class DummyEvent(object):
    def __init__(self, object):
        self.object = object


class TestSlackAction(unittest.TestCase):
    """Test case for SlackAction ."""

    layer = CONTENTRULES_SLACK_INTEGRATION_TESTING

    def _create_content(self, portal):
        """Create dummy content for our tests."""
        folder = api.content.create(
            type="Folder",
            id="folder",
            container=portal,
            title="Folder",
            description="A Folder",
        )
        doc = api.content.create(
            type="Document",
            id="d1",
            container=folder,
            title="A Document",
            description="A simple document",
        )
        self.folder = folder
        self.doc = doc

    def setUp(self):
        """Setup testcase."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self._create_content(self.portal)

    def test_registered(self):
        element = getUtility(IRuleAction, name="plone.actions.Slack")
        self.assertEqual("plone.actions.Slack", element.addview)
        self.assertEqual("edit", element.editview)
        self.assertEqual(None, element.for_)

    def test_invoke_add_View(self):
        element = getUtility(IRuleAction, name="plone.actions.Slack")
        storage = getUtility(IRuleStorage)
        storage[u"foo"] = Rule()
        rule = self.portal.restrictedTraverse("++rule++foo")
        adding = getMultiAdapter((rule, self.request), name="+action")
        addview = getMultiAdapter((adding, self.request), name=element.addview)
        self.assertTrue(isinstance(addview, SlackAddFormView))

        addview.form_instance.update()
        output = addview.form_instance()
        self.assertIn("<h2>Substitutions</h2>", output)
        content = addview.form_instance.create(data=ACTION_PAYLOAD)
        addview.form_instance.add(content)

        e = rule.actions[0]
        self.assertTrue(isinstance(e, SlackAction))
        self.assertIn("https://hooks.slack.com/", e.webhook_url)
        self.assertEqual("#tests", e.channel)
        self.assertEqual(ACTION_PAYLOAD["title"], e.title)
        self.assertEqual(ACTION_PAYLOAD["title_link"], e.title_link)
        self.assertEqual(ACTION_PAYLOAD["pretext"], e.pretext)
        self.assertEqual(ACTION_PAYLOAD["text"], e.text)
        self.assertEqual(ACTION_PAYLOAD["color"], e.color)
        self.assertEqual(ACTION_PAYLOAD["icon"], e.icon)
        self.assertEqual(ACTION_PAYLOAD["username"], e.username)
        self.assertEqual(ACTION_PAYLOAD["fields"], e.fields)

    def test_invoke_edit_view(self):
        element = getUtility(IRuleAction, name="plone.actions.Slack")
        e = SlackAction()
        editview = getMultiAdapter((e, self.request), name=element.editview)
        self.assertTrue(isinstance(editview, SlackEditFormView))

    def test_payload(self):
        e = SlackAction()
        for attr, value in ACTION_PAYLOAD.items():
            setattr(e, attr, value)

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.doc)), IExecutable)
        payload = ex.get_message_payload()
        self.assertEqual(u"Hello word! Private", payload["text"])

        attachment = payload["attachments"][0]
        fields = attachment["fields"]
        self.assertEqual(u"Document with title A Document", attachment["title"])
        self.assertEqual(2, len(fields))
        self.assertEqual(u"A Document", fields[0]["value"])

    def test_payload_with_none_values(self):
        e = SlackAction()
        for attr, value in ACTION_PAYLOAD.items():
            setattr(e, attr, value)

        e.title = None
        e.pretext = None

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.doc)), IExecutable)
        payload = ex.get_message_payload()

        attachment = payload["attachments"][0]
        fields = attachment["fields"]
        self.assertEqual(u"", attachment["title"])
        self.assertEqual(2, len(fields))
        self.assertEqual(u"A Document", fields[0]["value"])

    def test_execute(self):
        e = SlackAction()
        for attr, value in ACTION_PAYLOAD.items():
            setattr(e, attr, value)
        ex = getMultiAdapter((self.folder, e, DummyEvent(self.doc)), IExecutable)
        with RequestsMock.installed() as requests:
            payload = ex.get_payload()
            self.wait_for(ex.notify_slack(payload))
            self.assertEqual(1, len(requests.posts))
            post = requests.posts[0]
            self.assertEqual(ACTION_PAYLOAD["webhook_url"], post.get("url"))
            self.assertEqual(10, post.get("timeout"))
            self.assertTrue(post.get("verify"))
            self.assertTrue("text" in post.get("json"))
            self.assertTrue("attachments" in post.get("json"))

    def wait_for(self, thread):
        if not thread:
            return
        thread.join()
