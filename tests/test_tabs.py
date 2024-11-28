from __future__ import annotations

import pytest

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Tab, Tabs
from textual.widgets._tabs import Underline


class TabsMessageCatchApp(App[None]):
    def __init__(self) -> None:
        super().__init__()
        self.intended_handlers: list[str] = []

    def compose(self) -> ComposeResult:
        yield Tabs("John", "Aeryn", "Moya", "Pilot")

    @on(Tabs.Cleared)
    @on(Tabs.TabActivated)
    @on(Underline.Clicked)
    @on(Tab.Clicked)
    def log_message(
        self, event: Tabs.Cleared | Tabs.TabActivated | Underline.Clicked | Tab.Clicked
    ) -> None:
        self.intended_handlers.append(event.handler_name)

    @on(Tabs.TabActivated)
    @on(Tabs.Cleared)
    def check_control(self, event: Tabs.TabActivated) -> None:
        assert event.control is event.tabs


async def test_mouse_navigation_messages():
    """Mouse navigation should result in the expected messages."""
    async with TabsMessageCatchApp().run_test() as pilot:
        await pilot.click("#tab-2")
        await pilot.pause()
        await pilot.click("Underline", offset=(2, 0))
        await pilot.pause()
        assert pilot.app.intended_handlers == [
            "on_tabs_tab_activated",
            "on_tabs_tab_activated",
            "on_tabs_tab_activated",
        ]


async def test_disabled_tab_is_not_activated_by_clicking_underline():
    """Regression test for https://github.com/Textualize/textual/issues/4701"""

    class DisabledTabApp(App):
        def compose(self) -> ComposeResult:
            yield Tabs(
                Tab("Enabled", id="enabled"),
                Tab("Disabled", id="disabled", disabled=True),
            )

    app = DisabledTabApp()
    async with app.run_test() as pilot:
        # Click the underline beneath the disabled tab
        await pilot.click(Tabs, offset=(14, 2))
        tabs = pilot.app.query_one(Tabs)
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "enabled"
