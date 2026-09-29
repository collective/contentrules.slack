from . import ACTION_PAYLOAD
from . import DOCUMENT
from . import FOLDER
from collections.abc import Callable
from contentrules.slack import slack_notifier
from contentrules.slack.actions.slack import SlackAction
from contentrules.slack.slack_notifier import SlackNotifier
from contentrules.slack.testing import INTEGRATION_TESTING
from copy import deepcopy
from plone import api
from plone.dexterity.content import DexterityContent
from Products.CMFPlone.Portal import PloneSite
from pytest_plone import fixtures_factory
from threading import Thread

import pytest
import requests
import threading


pytest_plugins = ["pytest_plone"]


globals().update(fixtures_factory(((INTEGRATION_TESTING, "integration"),)))


class ResponseStub:
    """Stand-in for :class:`requests.Response`, answering with a status."""

    def __init__(self, status_code: int = 200) -> None:
        self.status_code = status_code

    def raise_for_status(self) -> None:
        """Mimic :meth:`requests.Response.raise_for_status`.

        :raises requests.HTTPError: When the status is 400 or above.
        """
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")


class RequestsRecorder:
    """Stand-in for the :mod:`requests` module, recording every post."""

    def __init__(self) -> None:
        self.posts: list[dict] = []
        self.status_code = 200

    def post(self, url: str, **kwargs) -> ResponseStub:
        """Record a post and answer with :attr:`status_code`.

        :param url: The URL posted to.
        :returns: A response stub.
        """
        self.posts.append({"url": url, **kwargs})
        return ResponseStub(self.status_code)


@pytest.fixture
def mock_requests(monkeypatch) -> RequestsRecorder:
    """Intercept the requests made by the notifier.

    :returns: The recorder; its ``posts`` lists the keyword arguments of each
        request, plus its ``url``.
    """
    recorder = RequestsRecorder()
    monkeypatch.setattr(slack_notifier, "requests", recorder)
    return recorder


@pytest.fixture
def wait_for() -> Callable[[Thread | None], None]:
    """Return a helper waiting for a notification thread to finish.

    :returns: Callable taking the value returned by ``notify_slack``; a
        ``None`` -- a deactivated notification -- returns at once.
    """

    def func(thread: Thread | None) -> None:
        if thread is not None:
            thread.join()

    return func


@pytest.fixture
def wait_for_notifications() -> Callable[[], None]:
    """Return a helper waiting for every running notification thread.

    For code paths that start a notification without handing the thread
    back, such as a content rule firing on an event.

    :returns: Callable taking no arguments.
    """

    def func() -> None:
        for thread in threading.enumerate():
            if thread.name == SlackNotifier.THREAD_NAME:
                thread.join()

    return func


@pytest.fixture
def folder(portal: PloneSite) -> DexterityContent:
    """Create the folder the rules are assigned to."""
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=portal, **FOLDER)


@pytest.fixture
def doc(folder: DexterityContent) -> DexterityContent:
    """Create a document inside :func:`folder`."""
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=folder, **DOCUMENT)


@pytest.fixture
def payload() -> dict:
    """Settings of a fully configured Slack action."""
    return deepcopy(ACTION_PAYLOAD)


@pytest.fixture
def slack_action(payload: dict) -> SlackAction:
    """Create a Slack action configured with :func:`payload`."""
    action = SlackAction()
    for attr, value in payload.items():
        setattr(action, attr, value)
    return action
