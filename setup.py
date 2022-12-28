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
    version="2.0.0.dev0",
    description="Slack content rule action for Plone.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Addon",
        "Framework :: Plone",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python",
    ],
    keywords="Python Plone Slack ContentRules Pendect",
    author="Pendect Tech",
    author_email="opensource@pendect.com",
    url="https://pypi.python.org/pypi/contentrules.slack",
    license="GPL version 2",
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/contentrules.slack',
        'Source': 'https://github.com/collective/contentrules.slack',
        'Tracker': 'https://github.com/collective/contentrules.slack/issues',
        'Documentation': 'https://contentrules.slack.readthedocs.io/en/latest/',
    },
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["contentrules"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7.0',
    install_requires=[
        "ftw.slacker>=1.1.0",
        "prettyconf",
        "plone.api",
        "setuptools",
    ],
    extras_require={
        "test": [
            "alabaster",
            "Jinja2",
            "snowballstemmer",
            "sphinx-bootstrap-theme",
            "Sphinx",
            "black",
            "isort",
            "zest.releaser[recommended]",
            "plone.app.testing",
            "plone.testing",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
