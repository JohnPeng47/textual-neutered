from __future__ import annotations

import pytest

from textual.app import App, ComposeResult
from textual.reactive import var
from textual.widgets import Label, Tab, TabbedContent, TabPane, Tabs
from textual.widgets._tabbed_content import ContentTab


async def test_tabs_nested_doesnt_interfere_with_ancestor_tabbed_content():
    """When a Tabs is nested as a descendant in the DOM of a TabbedContent,
    the messages posted from that Tabs should not interfere with the TabbedContent.
    A TabbedContent should only handle messages from Tabs which are direct children.

    Relates to https://github.com/Textualize/textual/issues/3412
    """

    class TabsNestedInTabbedContent(App):
        def compose(self) -> ComposeResult:
            with TabbedContent():
                with TabPane("OuterTab", id="outer1"):
                    yield Tabs(
                        Tab("Tab1", id="tab1"),
                        Tab("Tab2", id="tab2"),
                        id="inner-tabs",
                    )

    app = TabsNestedInTabbedContent()
    async with app.run_test():
        inner_tabs = app.query_one("#inner-tabs", Tabs)
        tabbed_content = app.query_one(TabbedContent)

        assert inner_tabs.active_tab.id == "tab1"
        assert tabbed_content.active == "outer1"

        await inner_tabs.clear()

        assert inner_tabs.active_tab is None
        assert tabbed_content.active == "outer1"


async def test_disabling_tab_within_tabbed_content_stays_isolated():
    """Disabling a tab within a tab pane should not affect the TabbedContent."""

    class TabsNestedInTabbedContent(App):
        def compose(self) -> ComposeResult:
            with TabbedContent():
                with TabPane("TabbedContent", id="duplicate"):
                    yield Tabs(
                        Tab("Tab1", id="duplicate"),
                        Tab("Tab2", id="stay-enabled"),
                        id="test-tabs",
                    )

    app = TabsNestedInTabbedContent()
    async with app.run_test() as pilot:
        assert app.query_one("Tab#duplicate").disabled is False
        assert app.query_one("TabPane#duplicate").disabled is False
        app.query_one("#test-tabs", Tabs).disable("duplicate")
        await pilot.pause()
        assert app.query_one("Tab#duplicate").disabled is True
        assert app.query_one("TabPane#duplicate").disabled is False
