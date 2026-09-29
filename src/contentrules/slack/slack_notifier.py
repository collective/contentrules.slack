"""Posting messages to Slack through incoming webhooks.

Requests run in a background thread, so a slow or unreachable Slack never
holds up the Plone request that triggered the notification.
"""

from contentrules.slack import logger
from contentrules.slack import settings
from contentrules.slack.interfaces import ISlackNotifier
from requests import RequestException
from threading import Thread
from typing import Any
from typing import cast
from zope.component import getUtility
from zope.interface import implementer

import requests


#: Use this value, as a webhook URL or in the ``DEACTIVATE_SLACK_NOTIFICATION``
#: environment variable, to deactivate notifications.
NOTIFICATION_DEACTIVATION_VALUE = "deactivate"


def notify_slack(
    webhook_url: str = "", timeout: int = 2, verify: bool = True, **payload: Any
) -> Thread | None:
    """Post a message to Slack using the registered :class:`ISlackNotifier`.

    Always use this function to send Slack notifications, so a replacement
    utility is honored.

    :param webhook_url: The Slack webhook URL. When empty, the value of the
        ``SLACK_WEBHOOK_URL`` environment variable is used instead.
    :param timeout: Seconds to wait for Slack before giving up.
    :param verify: Whether to verify SSL certificates.
    :param payload: Sent as the JSON payload of the request.
    :returns: The thread performing the request, or ``None`` when the
        notification is deactivated.
    """
    # Interface methods are declared without ``self``, so type checkers read
    # the utility through the signature of the default implementation.
    slacker = cast("SlackNotifier", getUtility(ISlackNotifier))
    return slacker.notify(webhook_url, timeout, verify, **payload)


@implementer(ISlackNotifier)
class SlackNotifier:
    """Default :class:`ISlackNotifier`, posting to a webhook in a thread."""

    #: Name of the thread performing the request.
    THREAD_NAME = "SlackNotifier-Thread"

    def notify(
        self,
        webhook_url: str = "",
        timeout: int = 2,
        verify: bool = True,
        **payload: Any,
    ) -> Thread | None:
        """Post a message to a Slack webhook in a background thread.

        :param webhook_url: The Slack webhook URL. When empty, the value of the
            ``SLACK_WEBHOOK_URL`` environment variable is used instead.
        :param timeout: Seconds to wait for Slack before giving up.
        :param verify: Whether to verify SSL certificates.
        :param payload: Sent as the JSON payload of the request.
        :returns: The started thread, or ``None`` when the notification is
            deactivated -- globally, or because no webhook URL is available.
        """
        if self._is_notification_globally_deactivated():
            return None

        webhook_url = self._choose_webhook_url(webhook_url)
        if self._is_notification_deactivated(webhook_url):
            return None

        thread = Thread(
            target=self._do_request,
            name=self.THREAD_NAME,
            args=(webhook_url, timeout, verify),
            kwargs=payload,
        )
        thread.start()
        return thread

    def _do_request(
        self,
        webhook_url: str = "",
        timeout: int = 2,
        verify: bool = True,
        **payload: Any,
    ) -> None:
        """Post the payload to the webhook, logging any failure.

        This runs in its own thread, where an exception would reach nobody
        but ``stderr``. Failures -- an error status from Slack, a timeout, a
        connection error -- are logged instead. The webhook URL is left out
        of the message: it is the credential that allows posting.

        :param webhook_url: The Slack webhook URL.
        :param timeout: Seconds to wait for Slack before giving up.
        :param verify: Whether to verify SSL certificates.
        :param payload: Sent as the JSON payload of the request.
        """
        try:
            requests.post(
                webhook_url,
                timeout=timeout,
                verify=verify,
                json=payload,
            ).raise_for_status()
        except RequestException as exc:
            logger.error(
                "Slack notification to channel %s failed: %s",
                payload.get("channel", "(default)"),
                exc.__class__.__name__,
            )

    def _choose_webhook_url(self, webhook_url: str) -> str:
        """Return the webhook URL to use.

        :param webhook_url: The webhook URL passed by the caller.
        :returns: ``webhook_url`` if set, otherwise the value of the
            ``SLACK_WEBHOOK_URL`` environment variable.
        """
        return webhook_url if webhook_url else settings.SLACK_WEBHOOK_URL

    def _is_notification_deactivated(self, webhook_url: str) -> bool:
        """Check if the notification is deactivated for a webhook URL.

        :param webhook_url: The webhook URL chosen for the request.
        :returns: ``True`` when the URL is empty or equals
            :data:`NOTIFICATION_DEACTIVATION_VALUE`, case-insensitively.
        """
        if not webhook_url:
            return True
        return webhook_url.lower() == NOTIFICATION_DEACTIVATION_VALUE

    def _is_notification_globally_deactivated(self) -> bool:
        """Check if notifications are deactivated for the whole instance.

        :returns: ``True`` when the ``DEACTIVATE_SLACK_NOTIFICATION``
            environment variable equals :data:`NOTIFICATION_DEACTIVATION_VALUE`,
            case-insensitively.
        """
        deactivate = settings.DEACTIVATE_SLACK_NOTIFICATION.lower()
        return deactivate == NOTIFICATION_DEACTIVATION_VALUE
