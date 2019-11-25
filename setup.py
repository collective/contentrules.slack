# -*- coding: utf-8 -*-
"""Installer for the contentrules.slack package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="contentrules.slack",
    version="1.0.0a2.dev0",
    description="Slack content rule action.",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone Slack ContentRules Briefy",
    author="Briefy Tech",
    author_email="developers@briefy.co",
    url="https://pypi.python.org/pypi/contentrules.slack",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["contentrules"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ftw.slacker",
        "plone.api",
        "prettyconf",
        "Products.GenericSetup>=1.8.2",
        "setuptools",
        "z3c.jbot",
    ],
    extras_require={
        "dev": ["zest.releaser[recommended]",],
        "test": [
            "plone.app.testing",
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
