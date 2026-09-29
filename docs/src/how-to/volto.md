---
myst:
  html_meta:
    "description": "How to post a message to Slack from a Plone content rule, using Volto."
    "property=og:description": "How to post a message to Slack from a Plone content rule, using Volto."
    "property=og:title": "Post to Slack with Volto"
    "keywords": "Plone, Slack, content rules, Volto"
---

# Post to Slack with Volto

This guide shows you how to create a content rule that posts a message to Slack, using {term}`Volto`.
As an example, the rule reports every user login to a Slack channel.

## Prerequisites

-   contentrules.slack is installed, as described in {doc}`install`.
-   You have a Slack {term}`incoming webhook` URL.
    To create one, follow Slack's guide [Sending messages using incoming webhooks](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/).

## Create the content rule

1.  Open {menuselection}`Site Setup --> Content Rules`.

    ```{image} /_static/images/volto/Screenshot-01.png
    :alt: The Content Rules control panel in Volto
    ```

2.  Select {guilabel}`Add content rule`.
3.  Enter a {guilabel}`Title`, such as `User Logged In`, and an optional {guilabel}`Description`.
4.  In {guilabel}`Triggering event`, select {guilabel}`User Logged in`, and save the form.

    ```{image} /_static/images/volto/Screenshot-02.png
    :alt: The form to add a content rule, with the User Logged in event selected
    ```

5.  In the list of rules, select {guilabel}`Configure` next to the new rule.

    ```{image} /_static/images/volto/Screenshot-03.png
    :alt: The list of content rules, with the new rule marked as not assigned
    ```

## Add the Slack action

1.  Under {guilabel}`Perform the following actions`, select {guilabel}`Post a message to Slack` in the {guilabel}`Action` list, and select {guilabel}`Add`.

    ```{image} /_static/images/volto/Screenshot-04.png
    :alt: The page to configure the content rule, with Post a message to Slack selected
    ```

2.  Fill in the form.
    {doc}`/reference/action` describes every field.

    ```{image} /_static/images/volto/Screenshot-05.png
    :alt: The empty form to add a Slack action
    ```

    Use `${...}` variables to include details about what triggered the rule.
    This example uses the full name of the user who logged in.

    ```{image} /_static/images/volto/Screenshot-06.png
    :alt: The Slack action form, filled in with the user_fullname variable
    ```

3.  Save the form.

The action appears under {guilabel}`Perform the following actions`.

```{image} /_static/images/volto/Screenshot-07.png
:alt: The page to configure the content rule, listing the Slack action
```

## Assign the rule

A rule runs only in the places it is assigned to.
To run it on the whole site, assign it at the site root.

1.  Go to the site root, and open {guilabel}`Rules` from the actions menu of the toolbar.
2.  In {guilabel}`Available content rules`, choose the rule, and select {guilabel}`Add`.

    ```{image} /_static/images/volto/Screenshot-08.png
    :alt: The content rules page of the site root, with the rule selected
    ```

The rule now appears as enabled, and applies to subfolders.

```{image} /_static/images/volto/Screenshot-09.png
:alt: The content rules page of the site root, listing the assigned rule
```

To run the rule only inside a folder, go to that folder, and assign the rule from its {guilabel}`Rules` page instead.

## Check the result

Log in to the site in another browser.
A message appears in the Slack channel.

```{image} /_static/images/classic-ui/Screenshot-07.png
:alt: The message posted to Slack after a user logged in
```

If no message appears, check the Plone backend log for errors from the `contentrules.slack` logger.
{doc}`/reference/python-api` lists the messages it writes.
