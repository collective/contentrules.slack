"""End to end: a content rule with a Slack action, fired by a real event."""

from contentrules.slack import settings
from contentrules.slack.slack_notifier import NOTIFICATION_DEACTIVATION_VALUE
from plone import api
from plone.app.contentrules import api as rules_api
from plone.app.contentrules.rule import Rule
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

import pytest


RULE_ID = "slack-on-modified"


@pytest.fixture
def rule(rule_storage, folder, slack_action) -> Rule:
    """Assign a rule posting to Slack whenever content in the folder changes."""
    rule = Rule()
    rule.title = "Slack on modified"
    rule.event = IObjectModifiedEvent
    rule.actions.append(slack_action)
    rule_storage[RULE_ID] = rule
    rules_api.assign_rule(folder, RULE_ID)
    return rule


@pytest.fixture
def modify(wait_for_notifications):
    """Return a helper firing a modified event and waiting for Slack."""

    def func(obj) -> None:
        notify(ObjectModifiedEvent(obj))
        wait_for_notifications()

    return func


@pytest.mark.usefixtures("rule")
class TestRule:
    def test_posts_when_content_is_modified(self, doc, modify, mock_requests):
        modify(doc)
        assert len(mock_requests.posts) == 1

    def test_message_is_about_the_modified_content(self, doc, modify, mock_requests):
        modify(doc)
        message = mock_requests.posts[0]["json"]
        attachment = message["attachments"][0]
        assert attachment["title"] == "Document with title A Document"
        assert attachment["title_link"] == doc.absolute_url()

    def test_content_outside_the_folder(self, portal, modify, mock_requests):
        with api.env.adopt_roles(["Manager"]):
            other = api.content.create(
                container=portal, type="Document", id="other", title="Other"
            )
        modify(other)
        assert mock_requests.posts == []

    def test_disabled_rule(self, rule, doc, modify, mock_requests):
        rule.enabled = False
        modify(doc)
        assert mock_requests.posts == []

    def test_globally_deactivated(self, monkeypatch, doc, modify, mock_requests):
        monkeypatch.setattr(
            settings, "DEACTIVATE_SLACK_NOTIFICATION", NOTIFICATION_DEACTIVATION_VALUE
        )
        modify(doc)
        assert mock_requests.posts == []
