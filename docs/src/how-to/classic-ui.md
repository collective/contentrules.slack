---
myst:
  html_meta:
    "description": "How to post a message to Slack from a Plone content rule, using Classic UI."
    "property=og:description": "How to post a message to Slack from a Plone content rule, using Classic UI."
    "property=og:title": "Post to Slack with Classic UI"
    "keywords": "Plone, Slack, content rules, Classic UI"
---

# Post to Slack with Classic UI

This guide shows you how to create a content rule that posts a message to Slack, using {term}`Classic UI`.
As an example, the rule reports every user login to a Slack channel.

## Prerequisites

-   contentrules.slack is installed, as described in {doc}`install`.
-   You have a Slack {term}`incoming webhook` URL.
    To create one, follow Slack's guide [Sending messages using incoming webhooks](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/).

## Create the content rule

1.  Open {menuselection}`Site Setup --> Content Rules`.

    ```{image} /_static/images/classic-ui/Screenshot-01.png
    :alt: The Content Rules control panel in Classic UI
    ```

2.  Select {guilabel}`Add content rule`.
3.  Enter a {guilabel}`Title`, such as `User Logged In`, and an optional {guilabel}`Description`.
4.  In {guilabel}`Triggering event`, select {guilabel}`User Logged in`.
5.  Select {guilabel}`Save`.

    ```{image} /_static/images/classic-ui/Screenshot-02.png
    :alt: The form to add a content rule, with the User Logged in event selected
    ```

## Add the Slack action

1.  On the page of the new rule, select {guilabel}`Post a message to Slack` in the {guilabel}`Action` list, and select {guilabel}`Add`.

    ```{image} /_static/images/classic-ui/Screenshot-03.png
    :alt: The page of the content rule, with the list of actions
    ```

2.  Fill in the form.
    {doc}`/reference/action` describes every field.

    ```{image} /_static/images/classic-ui/Screenshot-04.png
    :alt: The empty form to add a Slack action
    ```

    Use `${...}` variables to include details about what triggered the rule.
    The table at the bottom of the form lists the available variables.
    This example uses the full name and email of the user who logged in.

    ```{image} /_static/images/classic-ui/Screenshot-05.png
    :alt: The Slack action form, filled in with variables such as user_fullname and user_email
    ```

3.  Select {guilabel}`Save`.

The action appears under {guilabel}`Perform the following actions`.

## Assign the rule

A rule runs only in the places it is assigned to.
Select {guilabel}`Apply rule on the whole site` to run it everywhere.

```{image} /_static/images/classic-ui/Screenshot-06.png
:alt: The page of the content rule, with the Slack action and the Apply rule on the whole site button
```

To run the rule only inside a folder, go to that folder, open its {guilabel}`Rules` tab, and add the rule there.

## Check the result

Log in to the site in another browser.
A message appears in the Slack channel.

```{image} /_static/images/classic-ui/Screenshot-07.png
:alt: The message posted to Slack after a user logged in
```

If no message appears, check the Plone log for errors from the `contentrules.slack` logger.
{doc}`/reference/python-api` lists the messages it writes.
