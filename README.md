<div align="center"><img alt="logo" src="./docs/_static/images/icon.png" width="70" /></div>

<h1 align="center">contentrules.slack</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/contentrules.slack)](https://pypi.org/project/contentrules.slack/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/contentrules.slack)](https://pypi.org/project/contentrules.slack/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/contentrules.slack)](https://pypi.org/project/contentrules.slack/)
[![PyPI - License](https://img.shields.io/pypi/l/contentrules.slack)](https://pypi.org/project/contentrules.slack/)
[![PyPI - Status](https://img.shields.io/pypi/status/contentrules.slack)](https://pypi.org/project/contentrules.slack/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/contentrules.slack)](https://pypi.org/project/contentrules.slack/)

[![Code analysis checks](https://github.com/collective/contentrules.slack/actions/workflows/code-analysis.yml/badge.svg)](https://github.com/collective/contentrules.slack/actions/workflows/code-analysis.yml)
[![Tests](https://github.com/collective/contentrules.slack/actions/workflows/tests.yaml/badge.svg)](https://github.com/collective/contentrules.slack/actions/workflows/tests.yaml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/contentrules.slack)](https://github.com/collective/contentrules.slack)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/contentrules.slack?style=social)](https://github.com/collective/contentrules.slack)

</div>

Features
--------

**contentrules.slack** is a package providing a [Plone](https://plone.org/) content rules action to post a message on Slack.

Documentation
-------------

This package supports Plone sites using Volto and ClassicUI.

For proper Volto support, the requirements are:

* plone.restapi >= 8.34.0
* Volto >= 16.10.0

Installation
------------

Add **contentrules.slack** to the Plone installation using `pip`:

```bash
pip install contentrules.slack
```

or add it as a dependency on your package's `setup.py`

```python
    install_requires = [
        "contentrules.slack",
        "Plone",
        "plone.restapi",
        "setuptools",
    ],
```

Start Plone and go to the `Content Rules` Control Panel.

No additional configuration is needed for Volto support.


Source Code and Contributions
-----------------------------

If you want to help with the development (improvement, update, bug-fixing, ...) of `contentrules.slack` this is a great idea!

- [Issue Tracker](https://github.com/collective/contentrules.slack/issues)
- [Source Code](https://github.com/collective/contentrules.slack/)
- [Documentation](https://contentrulesslack.readthedocs.io/)


We appreciate any contribution and if a release is needed to be done on PyPI, please just contact one of us.

Development
-----------

You need a working `python` environment (system, virtualenv, pyenv, etc) version 3.8 or superior.

Then install the dependencies and a development instance using:

```bash
make build
```

To run tests for this package:
By default, we use the latest Plone version in the `6.x` series.

Translations
------------

This product has been translated into:

- English (Érico Andrei)
- Português do Brasil (Rudá Porto)
- Deutsch (Yael Biran)
- Español (Álvaro Hurtado Mochón)

License
-------

The project is licensed under GPLv2.

One Last Thing
--------------

Originally Made in Berlin, with love, by your friends @ Briefy and Pendect.

Now maintained by the [Plone Collective](https://github.com/collective)
