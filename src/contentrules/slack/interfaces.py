from zope.interface import Interface


class ISlackNotifier(Interface):
    """An ISlackNotifier utility is able to post messages through webhooks
    into a slack channel.
    """

    def notify(webhook_url, timeout, verify, **payload):
        """This method performs the slack-notification.

        :param webhook_url: The Slack webhook url
        :param timeout: Raises a timeout error after the given seconds.
        :param verify: verify ssl certificates on ssl connections.
        :param **payload: Additional keyword-arguments sent
                          as json-payload to the Slack webhook.

        See the slack documentation for all payload options:
        https://api.slack.com/incoming-webhooks
        """
