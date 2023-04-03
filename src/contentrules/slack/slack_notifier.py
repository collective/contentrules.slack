from contentrules.slack import settings
from contentrules.slack.interfaces import ISlackNotifier
from threading import Thread
from zope.component import getUtility
from zope.interface import implementer

import requests


def notify_slack(*args, **kwargs) -> Thread:
    """This is the main api function to perform a slack notification

    Always use this function to do slack notifications.

    See the readme.rst to find out how to use it.
    """
    slacker = getUtility(ISlackNotifier)
    return slacker.notify(*args, **kwargs)


# Use this string in your environment variables to deactivamete
# notification.
NOTIFICATION_DEACTIVATION_VALUE = "deactivate"


@implementer(ISlackNotifier)
class SlackNotifier:
    """The default slack notifier utility posts a message into slack through
    a webhook.
    """

    # Name of the request thread
    THREAD_NAME = "SlackNotifier-Thread"

    def notify(
        self, webhook_url: str = "", timeout: int = 2, verify: bool = True, **payload
    ) -> Thread:
        """Performs the slack notification"""
        if self._is_notification_globally_deactivated():
            return

        webhook_url = self._choose_webhook_url(webhook_url)
        if self._is_notification_deactivated(webhook_url):
            return

        thread = Thread(
            target=self._do_request,
            name=self.THREAD_NAME,
            args=(webhook_url, timeout, verify),
            kwargs=payload,
        )

        thread.start()
        return thread

    def _do_request(
        self, webhook_url: str = "", timeout: int = 2, verify: bool = True, **payload
    ):
        """Actually performs the request."""
        requests.post(
            webhook_url,
            timeout=timeout,
            verify=verify,
            json=payload,
        ).raise_for_status()

    def _choose_webhook_url(self, webhook_url: str) -> str:
        """Chooses the proper webhook_url. It returns the current
        webhook_url or a fallback value from an environment variable.
        """
        return webhook_url if webhook_url else settings.SLACK_WEBHOOK_URL

    def _is_notification_deactivated(self, webhook_url: str) -> bool:
        """Checks if the notification is deactivated based on the
        current webhook_url.
        """
        if not webhook_url:
            return True
        return webhook_url.lower() == NOTIFICATION_DEACTIVATION_VALUE

    def _is_notification_globally_deactivated(self) -> bool:
        """Checks if the notification is globally deactivated through
        an environment variable.
        """
        deactivate = settings.DEACTIVATE_SLACK_NOTIFICATION.lower()
        return deactivate == NOTIFICATION_DEACTIVATION_VALUE
