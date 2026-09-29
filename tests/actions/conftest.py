from collections.abc import Callable
from contentrules.slack.actions.slack import SlackAction
from contentrules.slack.actions.slack import SlackActionExecutor
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.dexterity.content import DexterityContent
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.lifecycleevent import ObjectModifiedEvent

import pytest


@pytest.fixture
def executor(
    folder: DexterityContent, doc: DexterityContent
) -> Callable[[SlackAction], SlackActionExecutor]:
    """Return a factory for the executor of an action.

    The executor is looked up as the content rules engine does, for an
    action assigned to :func:`folder` reacting to :func:`doc` being modified.

    :returns: Callable taking a Slack action and returning its executor.
    """

    def func(action: SlackAction) -> SlackActionExecutor:
        event = ObjectModifiedEvent(doc)
        return getMultiAdapter((folder, action, event), IExecutable)

    return func


@pytest.fixture
def rule_storage(portal) -> IRuleStorage:
    """Return the site's content rule storage."""
    return getUtility(IRuleStorage)
