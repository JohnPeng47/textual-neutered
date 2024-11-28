"""Unit tests dealing with the tracking of selection list values."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import SelectionList


class SelectionListApp(App[None]):
    def __init__(self, default_state: bool = False) -> None:
        super().__init__()
        self._default_state = default_state

    def compose(self) -> ComposeResult:
        yield SelectionList[int](*[(str(n), n, self._default_state) for n in range(50)])


async def test_programatic_toggle_all() -> None:
    """Selected should contain all values after toggling all on."""
    async with SelectionListApp().run_test() as pilot:
        selection = pilot.app.query_one(SelectionList)
        selection.toggle_all()
        assert pilot.app.query_one(SelectionList).selected == list(range(50))


async def test_removal_of_selected_item() -> None:
    """Removing a selected selection should remove its value from the selected set."""
    async with SelectionListApp().run_test() as pilot:
        selection = pilot.app.query_one(SelectionList)
        selection.toggle(0)
        assert pilot.app.query_one(SelectionList).selected == [0]
        selection.remove_option_at_index(0)
        assert pilot.app.query_one(SelectionList).selected == []
