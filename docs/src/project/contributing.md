---
myst:
  html_meta:
    "description": "How to set up a development environment for contentrules.slack, and run its tests, checks, and documentation."
    "property=og:description": "How to set up a development environment for contentrules.slack, and run its tests, checks, and documentation."
    "property=og:title": "Contributing"
    "keywords": "Plone, Slack, contributing, development"
---

# Contributing

Contributions to contentrules.slack are welcome, from bug reports to translations to code.

-   [Issue tracker](https://github.com/collective/contentrules.slack/issues)
-   [Source code](https://github.com/collective/contentrules.slack)
-   [Documentation](https://collective.github.io/contentrules.slack/)

## Prerequisites

-   [uv](https://docs.astral.sh/uv/)
-   GNU Make
-   Git

## Set up a development environment

Clone the repository and install it.

```shell
git clone https://github.com/collective/contentrules.slack.git
cd contentrules.slack
make install
```

`make install` creates a Python virtual environment in `.venv`, with Plone, this package, and the tools used for testing.
It also creates the configuration of a Plone instance in `instance/`.

To start that instance, and create a Plone site in it, run the following commands.

```shell
make create-site
make start
```

## Run the tests

```shell
make test
```

To also report test coverage, run the following command.
It fails when coverage drops below 95%.

```shell
make test-coverage
```

## Check the code

```shell
make format
make lint
```

`make format` rewrites the code in the project's style.
`make lint` checks it, and runs {term}`mypy` through `make mypy`.

## Build the documentation

```shell
make docs-html
```

The first `docs-*` command installs the documentation tools into `.venv`.
The HTML pages are written to `docs/_build/html`.
`make docs-livehtml` serves them, and rebuilds them on every change.
`make docs-vale` checks spelling and style.

## Update the translations

After you change a translatable string, update the translation catalogs.

```shell
make i18n
```

## Add a change log entry

Every change needs an entry in the change log.
Create a file in the `news/` folder, named after the GitHub issue number and the type of change, such as `news/42.bugfix`.

The type is one of `breaking`, `feature`, `bugfix`, `internal`, `documentation`, or `tests`.
The file contains one sentence describing the change, followed by your GitHub username.

```text
Fix the timeout of Slack requests. @your-github-username
```
