---
myst:
  html_meta:
    "description": "Why contentrules.slack posts to Slack in the background, what that means for failures, and why the webhook URL is treated as a secret."
    "property=og:description": "Why contentrules.slack posts to Slack in the background, what that means for failures, and why the webhook URL is treated as a secret."
    "property=og:title": "Message delivery"
    "keywords": "Plone, Slack, thread, delivery, webhook, security"
---

# Message delivery

A content rule runs inside the Plone request that triggered it.
When an editor publishes a page, the rule's actions run before Plone answers the editor's browser.
Anything slow in an action makes publishing slow, and anything that fails in an action can make publishing fail.

## Why messages are sent in the background

Slack is a remote service.
It usually answers within a fraction of a second, but it can be slow, and the network between Plone and Slack can fail.
If the action waited for Slack, every slow answer from Slack would become a slow page for the editor.

contentrules.slack avoids this by posting each message from its own thread.
The action starts the thread and returns at once, so the request that triggered the rule never waits for Slack.

## What happens when Slack fails

Sending in the background has a consequence: by the time Slack answers, the request that triggered the rule may already be over.
There is nobody left to show an error to, and the action has already told the content rules engine that it succeeded.

So a failure cannot stop the rule, and it cannot undo the change that triggered it.
Publishing a page succeeds even when Slack is down.
This is usually what you want, since a chat notification is rarely worth losing an edit over.

Instead, contentrules.slack writes each failure to the Plone log.
Before version 3.0, errors in the background thread went only to the standard error output of the process, where they were easy to miss.

## Why the webhook URL stays out of the log

An incoming webhook URL is a credential.
Anyone who has it can post to the channel, and Slack treats a leaked webhook URL as a leaked secret and may revoke it.

Log files are often shipped to other systems, and read by more people than those who configure content rules.
For that reason, the error message names the channel and the class of the error, but never the URL.

## Deactivating notifications

Copies of a production site are common: developers restore the database locally, and staging servers run the same content with the same rules.
Without care, those copies post to the production channels.

The `DEACTIVATE_SLACK_NOTIFICATION` setting exists for this case.
It switches off Slack for a whole Plone instance, from its environment, without editing the rules stored in the database.
{doc}`/how-to/deactivate-notifications` shows how to set it.
