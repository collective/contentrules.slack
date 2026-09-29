---
myst:
  html_meta:
    "description": "How to stop a Plone instance from posting to Slack, for example in development or staging."
    "property=og:description": "How to stop a Plone instance from posting to Slack, for example in development or staging."
    "property=og:title": "Deactivate Slack notifications"
    "keywords": "Plone, Slack, deactivate, staging, development"
---

# Deactivate Slack notifications

This guide shows you how to stop a Plone instance from posting to Slack, without changing its content rules.

Use it when you run a copy of a production database, for example in development or staging, so the copy does not post to the production channels.

## Set the environment variable

Set `DEACTIVATE_SLACK_NOTIFICATION` to `deactivate` in the environment of the Plone backend.

`````{tab-set}

````{tab-item} Shell
```shell
export DEACTIVATE_SLACK_NOTIFICATION=deactivate
```
````

````{tab-item} Docker Compose
```yaml
services:
  backend:
    environment:
      DEACTIVATE_SLACK_NOTIFICATION: deactivate
```
````

`````

The value is case-insensitive.
Any other value, or no value, leaves notifications active.

## Restart Plone

Restart the Plone backend.
contentrules.slack reads the variable once, at startup.

Content rules keep running, but their Slack actions post nothing.

## Reactivate notifications

Remove the variable, or set it to an empty value, and restart the Plone backend.

```{seealso}
{doc}`/reference/configuration` lists every setting, and where else they can be defined.
```
