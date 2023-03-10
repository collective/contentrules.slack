from contentrules.slack.testing import CRSLACK_INTEGRATION_TESTING
from plone import api
from pytest_plone import fixtures_factory

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(fixtures_factory(((CRSLACK_INTEGRATION_TESTING, "integration"),)))


@pytest.fixture(autouse=True)
def portal(integration):
    portal = integration["portal"]
    with api.env.adopt_roles(
        [
            "Manager",
        ]
    ):
        folder = api.content.create(
            type="Folder",
            id="folder",
            container=portal,
            title="Folder",
            description="A Folder",
        )
        api.content.create(
            type="Document",
            id="d1",
            container=folder,
            title="A Document",
            description="A simple document",
        )
    return portal


@pytest.fixture
def folder(portal):
    return portal.folder


@pytest.fixture
def doc(folder):
    return folder.d1


@pytest.fixture
def wait_for():
    def func(thread):
        if not thread:
            return
        thread.join()

    return func
