# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 3.0.0 (2026-09-29)


### Breaking

- Drop support for Plone 6.0 and Python 3.8 and 3.9. This package now requires Plone 6.1 or later, and Python 3.10 or later. @ericof [#14](https://github.com/collective/contentrules.slack/issues/14)


### Feature

- Log failed Slack notifications -- an error status, a timeout or a connection error -- to the `contentrules.slack` logger, instead of losing them in the background thread. The webhook URL is left out of the log message. @ericof [#17](https://github.com/collective/contentrules.slack/issues/17)


### Bugfix

- Add the missing space between the two sentences of the "Fields" help text, and update the translations to match. @ericof [#18](https://github.com/collective/contentrules.slack/issues/18)


### Internal

- Modernize the package with the cookieplone `backend_addon` template: `pyproject.toml` with hatchling, and a Makefile using uv and mxdev. Declare the `prettyconf` dependency explicitly. @ericof [#14](https://github.com/collective/contentrules.slack/issues/14)
- Add type hints and reStructuredText docstrings to the whole codebase, and check types with `mypy` against `plone-stubs` (`make mypy`, also run by `make lint`). @ericof [#15](https://github.com/collective/contentrules.slack/issues/15)
- Label Dependabot pull requests, and exempt them from the change log check. @ericof [#20](https://github.com/collective/contentrules.slack/issues/20)


### Documentation

- Rewrite the documentation following the Diátaxis framework, with how-to guides, a reference for the action, its configuration and its Python API, and an explanation of how messages are delivered. Publish it again on GitHub Pages, and rewrite the README for PyPI. @ericof [#19](https://github.com/collective/contentrules.slack/issues/19)


### Tests

- Reorganize the test suite, add end-to-end tests running a content rule with a Slack action on a real event, and require at least 95% test coverage. @ericof [#16](https://github.com/collective/contentrules.slack/issues/16)

## 2.0.2 (2023-04-04)


- Use `requests` instead of `httpx`, as the former is already distributed with Plone.
  [ericof]

- Update Sphinx theme used in the documentation
  [ericof]

## 2.0.1 (2023-03-10)


- Use [`pytest_plone`](https://pypi.org/project/pytest-plone/)
  [ericof]

- Deploy documentation to https://collective.github.io/contentrules.slack
  [ericof]



## 2.0.0 (2023-02-07)

- Use `pytest` instead of `unittest`
  [ericof]

- Drop dependency on `ftw.slacker`
  [ericof]

- Drop support to Plone 5.2
  [ericof]

- Support to Plone 6.0, Python 3.8 to 2.11
  [ericof]

- Update documentation
  [ericof]


## 1.0.1 (2020-04-25)

- Fix "TypeError: expected string or bytes-like object" when one attribute of action is not set.
  [ericof]


## 1.0.0 (2019-11-28)

- Add Plone 5.2 / Python 3 support.
  [ericof]

- Drop Python 2.7 support.
  [ericof]


## 1.0.0a1 (2017-10-17)

- Initial release.
  [ericof]
