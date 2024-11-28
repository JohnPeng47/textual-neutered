"""Unit tests aimed at testing the selection list messages.

Note that these tests only cover a subset of the public API of this widget.
The bulk of the API is inherited from OptionList, and as such there are
comprehensive tests for that. These tests simply cover the parts of the API
that have been modified by the child class.
"""

from __future__ import annotations

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import OptionList, SelectionList


class SelectionListApp(App[None]):
    """Test selection list application."""

    def __init__(self) -> None:
        super().__init__()
        self.messages: list[tuple[str, int | None]] = []

    def compose(self) -> ComposeResult:
        yield SelectionList[int](*[(str(n), n) for n in range(10)])

    @on(OptionList.OptionMessage)
    @on(SelectionList.SelectionMessage)
    @on(SelectionList.SelectedChanged)
    def _record(
        self,
        event: (
            OptionList.OptionMessage
            | SelectionList.SelectionMessage
            | SelectionList.SelectedChanged
        ),
    ) -> None:
        assert event.control == self.query_one(SelectionList)
        self.messages.append(
            (
                event.__class__.__name__,
                (
                    event.selection_index
                    if isinstance(event, SelectionList.SelectionMessage)
                    else None
                ),
            )
        )


async def test_deselect_all() -> None:
    """Deselecting all deselected options should result in no additional messages."""
    async with SelectionListApp().run_test() as pilot:
        assert isinstance(pilot.app, SelectionListApp)
        await pilot.pause()
        pilot.app.query_one(SelectionList).deselect_all()
        await pilot.pause()
        assert pilot.app.messages == [("SelectionHighlighted", 0)]


async def test_select_then_deselect_all() -> None:
    """Selecting and then deselecting all options should result in messages."""
    async with SelectionListApp().run_test() as pilot:
        assert isinstance(pilot.app, SelectionListApp)
        await pilot.pause()
        pilot.app.query_one(SelectionList).select_all()
        await pilot.pause()
        assert pilot.app.messages == [
            ("SelectionHighlighted", 0),
            ("SelectedChanged", None),
        ]
        pilot.app.query_one(SelectionList).deselect_all()
        await pilot.pause()
        assert pilot.app.messages == [
            ("SelectionHighlighted", 0),
            ("SelectedChanged", None),
            ("SelectedChanged", None),
        ]
