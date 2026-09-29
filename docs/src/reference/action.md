---
myst:
  html_meta:
    "description": "Fields of the Post a message to Slack content rule action, and the Slack message they produce."
    "property=og:description": "Fields of the Post a message to Slack content rule action, and the Slack message they produce."
    "property=og:title": "The Slack action"
    "keywords": "Plone, Slack, content rules, action, fields, payload"
---

(reference-action)=

# The Slack action

contentrules.slack registers one content rule action, {guilabel}`Post a message to Slack`, named `plone.actions.Slack`.

The action is available for every triggering event, and for every type of content.

## Fields

| Field | Required | Default | Interpolated | Sent to Slack as |
|---|---|---|---|---|
| {guilabel}`Webhook url` | Yes | None | No | The URL of the request |
| {guilabel}`Channel` | Yes | None | No | `channel` |
| {guilabel}`Pretext` | No | None | Yes | `attachments[0].pretext` |
| {guilabel}`Title` | Yes | None | Yes | `attachments[0].title` |
| {guilabel}`Title Link` | No | `${absolute_url}` | Yes | `attachments[0].title_link` |
| {guilabel}`Text` | Yes | None | Yes | `text` and `attachments[0].fallback` |
| {guilabel}`Color` | No | None | No | `attachments[0].color` |
| {guilabel}`Icon` | No | None | No | `icon_emoji` |
| {guilabel}`Username` | Yes | `Plone CMS` | No | `username` |
| {guilabel}`Fields` | No | None | Values only | `attachments[0].fields` |

Interpolated fields accept {term}`string interpolation` variables, such as `${title}` or `${user_fullname}`.
The variables are resolved against the object that triggered the rule.
The Classic UI form of the action lists every available variable.

Leading and trailing whitespace is removed from every interpolated value.
A field left empty is sent as an empty string.

{guilabel}`Webhook url`
:   Must be a URL, typically `https://hooks.slack.com/services/…`.

{guilabel}`Color`
:   One of `good`, `warning`, `danger`, or a hexadecimal color code such as `#439FE0`.

{guilabel}`Icon`
:   An emoji code, such as `:flag-br:`.

```{important}
Slack ignores {guilabel}`Channel`, {guilabel}`Icon`, and {guilabel}`Username` for incoming webhooks created by a Slack app.
Those webhooks always post to the channel, and with the name and icon, chosen when the app was installed.
Only legacy incoming webhooks honor these three fields.
```

(reference-action-fields-syntax)=

## Fields syntax

{guilabel}`Fields` adds a small table to the bottom of the message.
Define one table entry per line, in the format `title|value|short`.

```text
Title|${title}|True
Review State|${review_state_title}|False
```

`title`
:   The label of the entry.
    It is not interpolated.

`value`
:   The content of the entry.
    It is interpolated.

`short`
:   `True` displays the entry side by side with other short entries.
    The value is case-insensitive.
    Any value other than `true` counts as `False`.

A line that does not have exactly three parts, separated by `|`, is ignored.

## Message payload

The action sends a JSON payload to the webhook, such as the following example.

```json
{
  "attachments": [
    {
      "color": "good",
      "fallback": "Welcome to our friend Sebastião Salgado",
      "title": "Sebastião Salgado just logged in at Site",
      "title_link": "https://www.example.com/",
      "pretext": "User logged in",
      "fields": [
        {
          "title": "User email",
          "value": "salgado@not-really-a-mail.com",
          "short": false
        }
      ]
    }
  ],
  "icon_emoji": ":flag-br:",
  "text": "Welcome to our friend Sebastião Salgado",
  "username": "Plone CMS",
  "channel": "#plone-users"
}
```

The following image shows where each field appears in the message.

```{image} /_static/images/annotated-message.png
:alt: A Slack message, with each part labeled with the action field that produced it
```

## Request

The action posts the payload with a timeout of 10 seconds, and verifies SSL certificates.

The request runs in the background.
The action always reports success to the content rules engine, so the remaining actions of the rule run, whether Slack accepts the message or not.
Failures are logged, as described in {ref}`reference-python-api-logging`.
