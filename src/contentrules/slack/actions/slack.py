from contentrules.slack import _
from contentrules.slack.settings import SLACK_WEBHOOK_URL
from contentrules.slack.slack_notifier import notify_slack
from contentrules.slack.utils import extract_fields_from_text
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.stringinterp.dollarReplace import Interpolator
from plone.stringinterp.interfaces import IStringInterpolator
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from threading import Thread
from typing import Any
from typing import List
from zope import schema
from zope.component import adapter
from zope.i18nmessageid import Message
from zope.interface import implementer
from zope.interface import Interface

import logging


logger = logging.getLogger("contentrules.slack")


def safe_attr(element: "SlackAction", attr: str) -> Any:
    """Return attribute value as string."""
    value = getattr(element, attr)
    return value if value is not None else ""


class ISlackAction(Interface):
    """Definition of the configuration available for a slack action."""

    webhook_url = schema.URI(
        title=_("Webhook url"),
        description=_(
            "URL configuration for this integration. "
            'i.e.:"https://hooks.slack.com/services/T00000000/B00000000/YYYYYYYYYYYYYYYYYYYYYYYY"',  # noQA
        ),
        required=True,
    )
    channel = schema.TextLine(
        title=_("Channel"),
        description=_('Channel to receive the message. eg.:"#plone-rulez"'),
        required=True,
    )
    pretext = schema.TextLine(
        title=_("Pretext"),
        description=_(
            "This is optional text that appears above the message attachment block.",
        ),
        required=False,
    )
    title = schema.TextLine(
        title=_("Title"),
        description=_(
            "The title is displayed as larger, bold text near the top of a message attachment.",  # noQA
        ),
        required=True,
    )
    title_link = schema.TextLine(
        title=_("Title Link"),
        description=_('Link to be added to the title. i.e.: "${absolute_url}"'),
        default="${absolute_url}",
        required=False,
    )
    text = schema.TextLine(
        title=_("Text"),
        description=_("This is the main text in a message attachment."),
        required=True,
    )
    color = schema.TextLine(
        title=_("Color"),
        description=_(
            'Color of the message. Valid values are "good", "warning", "danger" or '
            "any hex color code (eg. #439FE0)",
        ),
        required=False,
    )
    icon = schema.TextLine(
        title=_("Icon"),
        description=_('Icon to be displayed on the message. eg:":flag-br:"'),
        required=False,
    )
    username = schema.TextLine(
        title=_("Username"),
        description=_("Name to be displayed as the author of this message."),
        default="Plone CMS",
        required=True,
    )
    fields = schema.Text(
        title=_("Fields"),
        description=_(
            "Fields are added to the bottom of the Slack message like a small table."
            'Please add one definition per line in the format:"title|value|Short", i.e:'
            '"Review State|${review_state_title}|True"',
        ),
        required=False,
    )


@implementer(ISlackAction, IRuleElementData)
class SlackAction(SimpleItem):
    """The implementation of the action defined before."""

    webhook_url: str = SLACK_WEBHOOK_URL
    channel: str = ""
    pretext: str = ""
    title: str = ""
    title_link: str = "${absolute_url}"
    text: str = ""
    color: str = ""
    icon: str = ""
    username: str = ""
    fields: str = ""

    element: str = "plone.actions.Slack"

    @property
    def summary(self) -> Message:
        return _(
            "Post a message on channel ${channel}",
            mapping=dict(channel=self.channel),
        )


@implementer(IExecutable)
@adapter(Interface, ISlackAction, Interface)
class SlackActionExecutor:
    """Executor for the Slack Action."""

    def __init__(self, context, element: "SlackAction", event):
        """Initialize action executor."""
        self.context = context
        self.element = element
        self.event = event

    def _process_fields_(self, interpolator: Interpolator) -> List[dict]:
        """Process element.fields and return a list of dicts.

        Read more at: https://api.slack.com/docs/message-attachments

        :returns: Message attachment fields.
        """
        element = self.element
        fields_spec = element.fields or ""
        fields = extract_fields_from_text(fields_spec)
        for item in fields:
            item["value"] = interpolator(item["value"]).strip()
        return fields

    def get_notifier_config(self) -> dict:
        """Return the configuration parameters used by ftw.slacker.

        :returns: Configuration parameters.
        """
        params = {
            "webhook_url": self.element.webhook_url,
            "timeout": 10,
            "verify": True,
        }
        return params

    def get_message_payload(self) -> dict:
        """Process the action and return a dictionary with the Slack message payload.

        :returns: Slack message payload.
        """
        obj = self.event.object
        element = self.element
        interpolator = IStringInterpolator(obj)
        title = interpolator(safe_attr(element, "title")).strip()
        title_link = interpolator(safe_attr(element, "title_link")).strip()
        pretext = interpolator(safe_attr(element, "pretext")).strip()
        text = interpolator(safe_attr(element, "text")).strip()
        color = safe_attr(element, "color")
        icon = safe_attr(element, "icon")
        channel = safe_attr(element, "channel")
        username = safe_attr(element, "username")
        payload = {
            "attachments": [
                {
                    "color": color,
                    "fallback": text,
                    "title": title,
                    "title_link": title_link,
                    "pretext": pretext,
                    "fields": self._process_fields_(interpolator),
                },
            ],
            "icon_emoji": icon,
            "text": text,
            "username": username,
            "channel": channel,
        }
        return payload

    def notify_slack(self, payload: dict) -> Thread:
        """Send message to Slack using ftw.slacker.notify_slack.

        :param payload: Payload to be sent to ftw.slacker.notify_slack.
        :type payload: dict
        """
        return notify_slack(**payload)

    def get_payload(self) -> dict:
        """Return payload to be sent to ftw.slacker.notify_slack.

        :returns: Payload to be sent to ftw.slacker.notify_slack.
        :rtype: dict
        """
        payload = self.get_message_payload()
        payload.update(self.get_notifier_config())
        return payload

    def __call__(self) -> bool:
        """Execute the action."""
        payload = self.get_payload()
        self.notify_slack(payload)
        return True


class SlackAddForm(ActionAddForm):
    """An add form for the Slack Action."""

    schema = ISlackAction
    label = _("Add Slack Action")
    description = _("Action to post a message to a Slack channel.")
    form_name = _("Configure element")
    Type = SlackAction

    # custom template will allow us to add help text
    template = ViewPageTemplateFile("slack.pt")


class SlackAddFormView(ContentRuleFormWrapper):
    """Wrapped add form for Slack Action."""

    form = SlackAddForm


class SlackEditForm(ActionEditForm):
    """An edit form for the slack action."""

    schema = ISlackAction
    label = _("Edit Slack Action")
    description = _("Action to post a message to a Slack channel.")
    form_name = _("Configure element")

    # custom template will allow us to add help text
    template = ViewPageTemplateFile("slack.pt")


class SlackEditFormView(ContentRuleFormWrapper):
    """Wrapped edit form for Slack Action."""

    form = SlackEditForm
