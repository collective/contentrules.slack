---
myst:
  html_meta:
    "description": "contentrules.slack adds a content rule action to Plone that posts a message to a Slack channel."
    "property=og:description": "contentrules.slack adds a content rule action to Plone that posts a message to a Slack channel."
    "property=og:title": "Slack integration for Plone"
    "keywords": "Plone, Slack, content rules, add-on, contentrules.slack"
---

# Slack integration for Plone

**contentrules.slack** is a {term}`Plone` {term}`add-on` that posts a message to a Slack channel whenever a {term}`content rule` runs.

Use it to tell a team when a page is published, when content is removed, when a user logs in, or on any other event Plone content rules support.
Messages can include details about the content or user that triggered the rule, such as its title, URL, or review state.

It works with both {term}`Volto` and {term}`Classic UI`, on Plone {SUPPORTED_PLONE_VERSIONS}, with Python {SUPPORTED_PYTHON_VERSIONS}.

```{image} /_static/images/classic-ui/Screenshot-07.png
:alt: A Slack message posted by Plone, announcing that a user logged in
```

## Documentation

`````{grid} 1 1 2 2
:gutter: 3

````{grid-item-card} 🛠️ How-to guides
:link: how-to/index
:link-type: doc

Install the add-on, and post to Slack from a content rule, in Volto or Classic UI.
````

````{grid-item-card} 📖 Reference
:link: reference/index
:link-type: doc

Fields of the action, the settings it reads, and its Python API.
````

````{grid-item-card} 💡 Explanation
:link: explanation/index
:link-type: doc

How messages reach Slack, and what happens when Slack fails.
````

````{grid-item-card} 🤝 Project
:link: project/index
:link-type: doc

Contributing, change log, translations, and license.
````

`````

```{toctree}
:maxdepth: 2
:hidden: true

how-to/index
reference/index
explanation/index
project/index
```

```{toctree}
:caption: Appendices
:maxdepth: 1
:hidden: true

glossary
genindex
```
