from __future__ import annotations

import pytest

from textual.app import App
from textual.widget import Widget, WidgetError


async def test_move_child_after_last_child() -> None:
    """Test moving after a child after the last child."""
    async with App().run_test() as pilot:
        widgets = [Widget(id=f"widget-{n}") for n in range(10)]
        container = Widget(*widgets)
        await pilot.app.mount(container)
        container.move_child(widgets[0], after=widgets[-1])
        assert container._nodes[0].id == "widget-1"
        assert container._nodes[-1].id == "widget-0"


async def test_move_child_after_last_numeric_location() -> None:
    """Test moving after a child after the last child's numeric position."""
    async with App().run_test() as pilot:
        widgets = [Widget(id=f"widget-{n}") for n in range(10)]
        container = Widget(*widgets)
        await pilot.app.mount(container)
        container.move_child(widgets[0], after=widgets[9])
        assert container._nodes[0].id == "widget-1"
        assert container._nodes[-1].id == "widget-0"
