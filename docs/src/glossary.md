---
myst:
  html_meta:
    "description": "Terms used in the contentrules.slack documentation."
    "property=og:description": "Terms used in the contentrules.slack documentation."
    "property=og:title": "Glossary"
    "keywords": "Plone, Slack, glossary"
---

(glossary-label)=

# Glossary

```{glossary}
:sorted: true

Plone
    [Plone](https://plone.org/) is an open source content management system, used to build websites, intranets, and custom applications.

add-on
    A Python package that extends the functionality of Plone.

content rule
    A Plone feature that runs actions when an event happens, such as content being published or a user logging in.
    A rule has a triggering event, optional conditions, and one or more actions, and runs only in the locations it is assigned to.

incoming webhook
    A URL provided by Slack that accepts messages for a channel through an HTTP `POST` request.
    See [Sending messages using incoming webhooks](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/) in the Slack documentation.

string interpolation
    Replacing `${...}` variables in a text with values from the object that triggered a content rule, such as `${title}` or `${absolute_url}`.
    Plone provides this through the `plone.stringinterp` package.

Classic UI
    The server-rendered user interface of Plone, built with page templates.

Volto
    The React-based user interface of Plone.

mypy
    A static type checker for Python.
```
