from prettyconf import config


SLACK_WEBHOOK_URL = config("SLACK_WEBHOOK_URL", default="")
DEACTIVATE_SLACK_NOTIFICATION = config("DEACTIVATE_SLACK_NOTIFICATION", default="")
