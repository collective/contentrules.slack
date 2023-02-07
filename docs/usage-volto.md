# Using Volto

Go to the Site Setup, then click on Content Rules.

```{image} ./_static/images/volto/Screenshot-01.png
:align: center
:alt: Content rules control panel
```

Click on **Add content rule** and a form to create a new content rule will be displayed.

We are going to create a content rule to report every time an user logs in to a Plone portal.

```{image} ./_static/images/volto/Screenshot-02.png
:align: center
:alt: A form to add a new content rule
```
After saving the form, it will be possible to configure the conditions and actions of this content rule.

For this example we will only add an action to **Post a message to Slack**, select this option and click **Add**

```{image} ./_static/images/volto/Screenshot-03.png
:align: center
:alt: Edit content rule page
```

This will bring a form to configure the content rule action.

```{image} ./_static/images/volto/Screenshot-04.png
:align: center
:alt: Add action form
```

Here is a breakdown of how fields setting in this form will affect the message on Slack.

```{image} ./_static/images/annotated-message.png
:align: center
:alt: Annoted message
```

It is possible to use variables on some fields, as displayed here.

```{image} ./_static/images/volto/Screenshot-05.png
:align: center
:alt: Filled Add action form
```

Saving the action form, will bring us back to the content rule configuration.

```{image} ./_static/images/volto/Screenshot-06.png
:align: center
:alt: Apply rule on site
```

Now, apply this rule to the whole site.

The next user login will sent a message on the Slack channel.

```{image} ./_static/images/volto/Screenshot-07.png
:align: center
:alt: Message on Slack
```
