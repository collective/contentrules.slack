"""The action is offered by the control panel, with its add and edit forms."""

from contentrules.slack.actions.slack import ISlackAction
from contentrules.slack.actions.slack import SlackAction
from contentrules.slack.actions.slack import SlackAddFormView
from contentrules.slack.actions.slack import SlackEditFormView
from plone.app.contentrules.rule import Rule
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IRuleElementData
from zope.component import getMultiAdapter
from zope.component import getUtility

import pytest


ACTION_NAME = "plone.actions.Slack"


@pytest.fixture
def element(portal) -> IRuleAction:
    """The rule element registered for the Slack action."""
    return getUtility(IRuleAction, name=ACTION_NAME)


@pytest.fixture
def rule(portal, rule_storage) -> Rule:
    """Create an empty rule, traversed as the control panel does."""
    rule_storage["foo"] = Rule()
    return portal.restrictedTraverse("++rule++foo")


class TestRegistration:
    def test_registered(self, element):
        assert element.addview == ACTION_NAME
        assert element.editview == "edit"
        assert element.schema is ISlackAction
        assert element.factory is SlackAction

    def test_available_for_any_event_and_content(self, element):
        assert element.for_ is None
        assert element.event is None

    def test_fields_description(self):
        """The two sentences of the help text used to run together."""
        description = ISlackAction["fields"].description
        assert "like a small table. Please add one definition" in description


class TestSlackAction:
    def test_provides_interfaces(self):
        action = SlackAction()
        assert ISlackAction.providedBy(action)
        assert IRuleElementData.providedBy(action)

    def test_element(self):
        assert SlackAction().element == ACTION_NAME

    def test_summary(self, slack_action):
        summary = slack_action.summary
        assert summary == "Post a message on channel ${channel}"
        assert summary.mapping == {"channel": "#tests"}

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ["title_link", "${absolute_url}"],
            ["channel", ""],
            ["username", ""],
            ["fields", ""],
        ],
    )
    def test_defaults(self, attr, expected):
        assert getattr(SlackAction(), attr) == expected


class TestAddForm:
    def test_view(self, rule, element, http_request):
        adding = getMultiAdapter((rule, http_request), name="+action")
        addview = getMultiAdapter((adding, http_request), name=element.addview)
        assert isinstance(addview, SlackAddFormView)

    def test_renders_the_help_text(self, rule, element, http_request):
        adding = getMultiAdapter((rule, http_request), name="+action")
        addview = getMultiAdapter((adding, http_request), name=element.addview)
        addview.form_instance.update()
        output = addview.form_instance()
        assert "<h2>Slack Configuration</h2>" in output
        assert "<h2>Substitutions</h2>" in output

    def test_add(self, rule, element, http_request, payload):
        adding = getMultiAdapter((rule, http_request), name="+action")
        addview = getMultiAdapter((adding, http_request), name=element.addview)
        form = addview.form_instance
        # The form only knows its fields -- and so only applies data -- once
        # updated.
        form.update()
        form.add(form.create(data=payload))

        action = rule.actions[0]
        assert isinstance(action, SlackAction)
        for attr, value in payload.items():
            assert getattr(action, attr) == value


class TestEditForm:
    def test_view(self, element, http_request):
        editview = getMultiAdapter((SlackAction(), http_request), name=element.editview)
        assert isinstance(editview, SlackEditFormView)
