"""Settings read once, when the package is imported.

Values are read by `prettyconf <https://prettyconf.readthedocs.io>`_.
An environment variable wins. Otherwise prettyconf looks for the variable in
``.env`` files, then in the ``[settings]`` section of ``*.ini`` and ``*.cfg``
files, starting in the directory of this package and moving up through each
of its parents.
"""

from prettyconf import config


#: Webhook used when an action, or a direct call to
#: :func:`contentrules.slack.slack_notifier.notify_slack`, names none.
SLACK_WEBHOOK_URL: str = config("SLACK_WEBHOOK_URL", default="")

#: Set to ``deactivate`` to switch off every Slack notification in the
#: instance -- useful for development and staging environments.
DEACTIVATE_SLACK_NOTIFICATION: str = config("DEACTIVATE_SLACK_NOTIFICATION", default="")
