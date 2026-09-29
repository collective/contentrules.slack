---
myst:
  html_meta:
    "description": "Environment variables read by contentrules.slack, and where they can be defined."
    "property=og:description": "Environment variables read by contentrules.slack, and where they can be defined."
    "property=og:title": "Configuration"
    "keywords": "Plone, Slack, configuration, environment variables"
---

(reference-configuration)=

# Configuration

contentrules.slack reads two settings.
It reads them once, when Plone starts, so you must restart Plone after changing them.

## Settings

`DEACTIVATE_SLACK_NOTIFICATION`
:   Set to `deactivate`, case-insensitive, to deactivate every Slack notification of the Plone instance.
    Content rules keep running, but their Slack actions post nothing.
    Any other value leaves notifications active.

    Default: empty.

`SLACK_WEBHOOK_URL`
:   The webhook used when a call to {py:func}`contentrules.slack.slack_notifier.notify_slack` does not pass one.
    Content rule actions do not use it, because their {guilabel}`Webhook url` field is required.

    Default: empty.

## Where settings are read from

contentrules.slack reads its settings with [prettyconf](https://prettyconf.readthedocs.io/en/latest/).
For each setting, the first of these sources that defines it wins.

1.  An environment variable of the Plone process.
2.  A `.env` file.
3.  The `[settings]` section of a `*.ini` or `*.cfg` file.

prettyconf searches for these files in the directory of the installed `contentrules.slack` package, then in each of its parent directories, up to the root of the file system.
In each directory, it reads `.env` files before `*.ini` and `*.cfg` files.

```{warning}
The search runs from where the package is installed, not from the working directory of Plone.
A `.env` file next to your `instance` folder is read only if that folder is a parent of the Python environment Plone runs in.
Use environment variables when in doubt.
```

## Webhook deactivation value

`deactivate`, case-insensitive, also deactivates a single notification when it is passed as the webhook URL to {py:func}`~contentrules.slack.slack_notifier.notify_slack`.
