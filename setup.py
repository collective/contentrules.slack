"""Installer for the contentrules.slack package."""
from pathlib import Path
from setuptools import find_packages
from setuptools import setup


long_description = f"""
{Path("README.md").read_text()}\n
{Path("CONTRIBUTORS.md").read_text()}\n
{Path("CHANGES.md").read_text()}\n
"""


setup(
    name="contentrules.slack",
    version="2.0.2.dev0",
    description="Slack content rule action for Plone.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone Slack ContentRules Pendect",
    author="Pendect Tech",
    author_email="opensource@pendect.com",
    url="https://pypi.python.org/pypi/contentrules.slack",
    license="GPL version 2",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/contentrules.slack",
        "Source": "https://github.com/collective/contentrules.slack",
        "Tracker": "https://github.com/collective/contentrules.slack/issues",
        "Documentation": "https://collective.github.io/contentrules.slack",
    },
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["contentrules"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8.0",
    install_requires=[
        "httpx",
        "prettyconf",
        "Plone",
        "setuptools",
        "plone.restapi>=8.34.0",
    ],
    extras_require={
        "test": [
            "gocept.pytestlayer",
            "plone.app.robotframework[debug]",
            "plone.app.testing",
            "plone.restapi[test]",
            "pytest-cov",
            "pytest-plone>=0.2.0",
            "pytest",
            "zest.releaser[recommended]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_cr_slack_locale = contentrules.slack.locales.update:update_locale
    """,
)
