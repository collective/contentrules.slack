---
myst:
  html_meta:
    "description": "Python API of contentrules.slack: sending Slack notifications from code, and the log messages it writes."
    "property=og:description": "Python API of contentrules.slack: sending Slack notifications from code, and the log messages it writes."
    "property=og:title": "Python API"
    "keywords": "Plone, Slack, Python, API, notify_slack, logging"
---

(reference-python-api)=

# Python API

You can post to Slack from your own code, without a content rule.

```python
from contentrules.slack.slack_notifier import notify_slack

notify_slack(
    "https://hooks.slack.com/services/T.../B.../...",
    text="The nightly import finished.",
)
```

Every keyword argument other than `webhook_url`, `timeout`, and `verify` becomes part of the JSON payload.
See Slack's [message payload reference](https://docs.slack.dev/messaging/formatting-message-text/) for the keys Slack accepts.

## Notifier

```{eval-rst}
.. autofunction:: contentrules.slack.slack_notifier.notify_slack

.. autodata:: contentrules.slack.slack_notifier.NOTIFICATION_DEACTIVATION_VALUE
   :no-value:

.. autoclass:: contentrules.slack.interfaces.ISlackNotifier

   Its ``notify`` method has the signature of :py:meth:`SlackNotifier.notify`.
   Register a utility providing this interface to replace how messages are sent.

.. autoclass:: contentrules.slack.slack_notifier.SlackNotifier
   :members: notify, THREAD_NAME
```

## Helpers

```{eval-rst}
.. autofunction:: contentrules.slack.utils.extract_fields_from_text
```

(reference-python-api-logging)=

## Logging

contentrules.slack writes to the `contentrules.slack` logger.

When a request to Slack fails, it logs the following message at the `ERROR` level.

```text
Slack notification to channel <channel> failed: <error>
```

`<channel>`
:   The `channel` of the payload, or `(default)` when the payload has none.

`<error>`
:   The class of the error, such as `HTTPError` for an error status from Slack, `Timeout`, or `ConnectionError`.

The message never includes the webhook URL.
