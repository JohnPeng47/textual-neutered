from __future__ import annotations

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Collapsible, Label
from textual.widgets._collapsible import CollapsibleTitle

COLLAPSED_CLASS = "-collapsed"


def get_title(collapsible: Collapsible) -> CollapsibleTitle:
    return collapsible.get_child_by_type(CollapsibleTitle)


def get_contents(collapsible: Collapsible) -> Collapsible.Contents:
    return collapsible.get_child_by_type(Collapsible.Contents)


async def test_collapse_via_watcher_message():
    """Setting `collapsed` to `True` should post a message."""

    hits = []

    class CollapsibleApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Collapsible(collapsed=False)

        def on_collapsible_collapsed(self) -> None:
            hits.append("collapsed")

    async with CollapsibleApp().run_test() as pilot:
        assert not pilot.app.query_one(Collapsible).collapsed

        pilot.app.query_one(Collapsible).collapsed = True
        await pilot.pause()

        assert pilot.app.query_one(Collapsible).collapsed
        assert len(hits) == 1


async def test_collapsible_title_reactive_change():
    class CollapsibleApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Collapsible(title="Old title")

    async with CollapsibleApp().run_test() as pilot:
        collapsible = pilot.app.query_one(Collapsible)
        assert get_title(collapsible).label == "Old title"
        collapsible.title = "New title"
        assert get_title(collapsible).label == "New title"
