"""Shared values for the contentrules.slack test suite.

Payloads live here rather than in ``conftest.py`` so they can be imported
relatively from any test package: ``from tests import WEBHOOK_URL``. The
fixtures that hand them out are in :mod:`tests.conftest`.
"""

from typing import Any


#: Webhook used by tests; requests to it are always intercepted.
WEBHOOK_URL = "https://hooks.slack.com/services/TEST/WEBHOOK/URL"

#: Settings of the Slack action created by the ``slack_action`` fixture.
ACTION_PAYLOAD: dict[str, Any] = {
    "webhook_url": WEBHOOK_URL,
    "channel": "#tests",
    "pretext": "What about this new document?",
    "title": "Document with title ${title}",
    "title_link": "${absolute_url}",
    "text": "Hello world! ${review_state_title}",
    "color": "danger",
    "icon": ":flag-br:",
    "username": "Plone Butler",
    "fields": "Title|${title}|True\nReview State|${review_state_title}|False",
}

#: Folder the rule is assigned to, created by the ``folder`` fixture.
FOLDER: dict[str, Any] = {
    "type": "Folder",
    "id": "folder",
    "title": "Folder",
    "description": "A Folder",
}

#: Document the messages are about, created by the ``doc`` fixture.
DOCUMENT: dict[str, Any] = {
    "type": "Document",
    "id": "d1",
    "title": "A Document",
    "description": "A simple document",
}
