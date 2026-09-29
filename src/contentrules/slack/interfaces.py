"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface


class ISlackNotifier(Interface):
    """A utility posting messages into a Slack channel through a webhook."""

    def notify(webhook_url, timeout, verify, **payload):
        """Post a message to a Slack webhook.

        See the Slack documentation for all payload options:
        https://api.slack.com/messaging/webhooks

        :param webhook_url: The Slack webhook URL. When empty, the value of the
            ``SLACK_WEBHOOK_URL`` environment variable is used instead.
        :param timeout: Seconds to wait for Slack before giving up.
        :param verify: Whether to verify SSL certificates.
        :param payload: Additional keyword arguments, sent as the JSON payload
            of the request.
        :returns: The thread performing the request, or ``None`` when the
            notification is deactivated.
        """
