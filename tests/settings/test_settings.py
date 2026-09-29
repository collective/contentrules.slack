"""Settings are read from the environment when the module is imported."""

from collections.abc import Callable
from collections.abc import Generator
from contentrules.slack import settings
from types import ModuleType

import importlib
import pytest


@pytest.fixture
def reload_settings(monkeypatch) -> Generator[Callable[..., ModuleType], None, None]:
    """Return a helper re-importing the settings under a given environment.

    The module is re-imported once more afterwards, with the environment
    restored, so later tests see the original values.

    :returns: Callable taking environment variables as keyword arguments and
        returning the reloaded module.
    """

    def func(**environ: str) -> ModuleType:
        for key in ("SLACK_WEBHOOK_URL", "DEACTIVATE_SLACK_NOTIFICATION"):
            monkeypatch.delenv(key, raising=False)
        for key, value in environ.items():
            monkeypatch.setenv(key, value)
        return importlib.reload(settings)

    yield func
    monkeypatch.undo()
    importlib.reload(settings)


class TestSettings:
    def test_defaults(self, reload_settings):
        module = reload_settings()
        assert module.SLACK_WEBHOOK_URL == ""
        assert module.DEACTIVATE_SLACK_NOTIFICATION == ""

    def test_webhook_url(self, reload_settings):
        module = reload_settings(SLACK_WEBHOOK_URL="https://hooks.slack.com/foo")
        assert module.SLACK_WEBHOOK_URL == "https://hooks.slack.com/foo"

    def test_deactivate(self, reload_settings):
        module = reload_settings(DEACTIVATE_SLACK_NOTIFICATION="deactivate")
        assert module.DEACTIVATE_SLACK_NOTIFICATION == "deactivate"
