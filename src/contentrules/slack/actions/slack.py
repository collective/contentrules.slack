"""Content rule action posting a message to a Slack channel.

The action is configured through the content rules control panel. Its text
settings accept ``${...}`` string interpolation variables, which are resolved
against the object that triggered the rule when the action runs.
"""

from collections.abc import Callable
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
from plone.stringinterp.interfaces import IStringInterpolator
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from threading import Thread
from typing import Any
from typing import cast
from zope import schema
from zope.component import adapter
from zope.i18nmessageid import Message
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.interfaces import IObjectEvent


#: Resolves the ``${...}`` variables of a string against an object.
Interpolator = Callable[[str], str]


def safe_attr(element: "SlackAction", attr: str) -> str:
    """Read an action setting, treating ``None`` as an empty string.

    Optional fields are stored as ``None`` when left empty in the form.

    :param element: The Slack action.
    :param attr: Name of the setting.
    :returns: The setting's value, or ``""`` when it is ``None``.
    """
    value = getattr(element, attr)
    return value if value is not None else ""


class ISlackAction(Interface):
    """Definition of the configuration available for a slack action."""

    webhook_url = schema.URI(
        title=_("Webhook url"),
        description=_(
            "URL configuration for this integration. "
            'i.e.:"https://hooks.slack.com/services/T.../B.../..."',
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
            "The title is displayed as larger, bold text near the top of a message attachment.",  # noqa: E501
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
            "Fields are added to the bottom of the Slack message like a small table. "
            'Please add one definition per line in the format:"title|value|Short", i.e:'
            '"Review State|${review_state_title}|True"',
        ),
        required=False,
    )


@implementer(ISlackAction, IRuleElementData)
class SlackAction(SimpleItem):
    """Persistent settings of a Slack action, stored in a content rule."""

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
        """Describe the action in the content rule's list of actions.

        :returns: Translatable summary naming the target channel.
        """
        return _(
            "Post a message on channel ${channel}",
            mapping={"channel": self.channel},
        )


@implementer(IExecutable)
@adapter(Interface, ISlackAction, Interface)
class SlackActionExecutor:
    """Run a Slack action for the object that triggered a content rule."""

    def __init__(self, context: Any, element: SlackAction, event: IObjectEvent):
        """Initialize the executor.

        :param context: Container where the rule is assigned.
        :param element: The Slack action.
        :param event: The event that triggered the rule. Its ``object`` is
            the content the message is about.
        """
        self.context = context
        self.element = element
        self.event = event

    def _process_fields(self, interpolator: Interpolator) -> list[dict]:
        """Build the attachment fields, interpolating each value.

        Read more at: https://api.slack.com/reference/messaging/attachments

        :param interpolator: Resolves ``${...}`` variables against the
            triggering object.
        :returns: Message attachment fields.
        """
        fields = extract_fields_from_text(self.element.fields or "")
        for item in fields:
            item["value"] = interpolator(item["value"]).strip()
        return fields

    def get_notifier_config(self) -> dict:
        """Return the request settings for :func:`notify_slack`.

        :returns: Webhook URL, timeout and SSL verification settings.
        """
        return {
            "webhook_url": self.element.webhook_url,
            "timeout": 10,
            "verify": True,
        }

    def get_message_payload(self) -> dict:
        """Build the Slack message for the triggering object.

        :returns: Slack message payload.
        """
        obj = self.event.object
        element = self.element
        interpolator = cast(Interpolator, IStringInterpolator(obj))
        title = interpolator(safe_attr(element, "title")).strip()
        title_link = interpolator(safe_attr(element, "title_link")).strip()
        pretext = interpolator(safe_attr(element, "pretext")).strip()
        text = interpolator(safe_attr(element, "text")).strip()
        color = safe_attr(element, "color")
        icon = safe_attr(element, "icon")
        channel = safe_attr(element, "channel")
        username = safe_attr(element, "username")
        return {
            "attachments": [
                {
                    "color": color,
                    "fallback": text,
                    "title": title,
                    "title_link": title_link,
                    "pretext": pretext,
                    "fields": self._process_fields(interpolator),
                },
            ],
            "icon_emoji": icon,
            "text": text,
            "username": username,
            "channel": channel,
        }

    def notify_slack(self, payload: dict) -> Thread | None:
        """Send a message to Slack.

        :param payload: Keyword arguments for :func:`notify_slack`, as
            returned by :meth:`get_payload`.
        :returns: The thread performing the request, or ``None`` when the
            notification is deactivated.
        """
        return notify_slack(**payload)

    def get_payload(self) -> dict:
        """Combine the message payload and the request settings.

        :returns: Keyword arguments for :func:`notify_slack`.
        """
        payload = self.get_message_payload()
        payload.update(self.get_notifier_config())
        return payload

    def __call__(self) -> bool:
        """Execute the action.

        The request runs in the background, so the result reflects only that
        the message was handed over, not that Slack accepted it.

        :returns: Always ``True``, so the rule's remaining actions run.
        """
        self.notify_slack(self.get_payload())
        return True


class SlackAddForm(ActionAddForm):
    """An add form for the Slack Action."""

    schema = ISlackAction  # type: ignore[assignment]
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

    schema = ISlackAction  # type: ignore[assignment]
    label = _("Edit Slack Action")
    description = _("Action to post a message to a Slack channel.")
    form_name = _("Configure element")

    # custom template will allow us to add help text
    template = ViewPageTemplateFile("slack.pt")


class SlackEditFormView(ContentRuleFormWrapper):
    """Wrapped edit form for Slack Action."""

    form = SlackEditForm
