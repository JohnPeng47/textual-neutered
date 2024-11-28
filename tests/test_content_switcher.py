from __future__ import annotations

import pytest

from textual.app import App, ComposeResult
from textual.css.query import NoMatches
from textual.widget import Widget
from textual.widgets import ContentSwitcher


class SwitcherApp(App[None]):
    def __init__(self, initial: str | None = None) -> None:
        super().__init__()
        self._initial = initial

    def compose(self) -> ComposeResult:
        with ContentSwitcher(initial=self._initial):
            for n in range(5):
                yield Widget(id=f"w{n}")


async def test_set_current_to_unknown_id() -> None:
    """Test attempting to switch to an unknown widget ID."""
    async with SwitcherApp().run_test() as pilot:
        assert pilot.app.query_one(ContentSwitcher).current is None
        assert all(
            not child.display for child in pilot.app.query_one(ContentSwitcher).children
        )
        with pytest.raises(NoMatches):
            pilot.app.query_one(ContentSwitcher).current = "does-not-exist"


async def test_add_content() -> None:
    async with SwitcherApp().run_test() as pilot:
        switcher = pilot.app.query_one(ContentSwitcher)
        await switcher.add_content(Widget(id="foo"))
        assert not switcher.query_one("#foo").display
        await switcher.add_content(Widget(), id="bar", set_current=True)
        assert not switcher.query_one("#foo").display
        assert switcher.query_one("#bar").display
        assert switcher.current == "bar"
        with pytest.raises(ValueError):
            switcher.add_content(Widget())
