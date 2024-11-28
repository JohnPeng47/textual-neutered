"""Core selection list unit tests, aimed at testing basic list creation.

Note that the vast majority of the API *isn't* tested in here as
`SelectionList` inherits from `OptionList` and so that would be duplicated
effort. Instead these tests aim to just test the things that have been
changed or wrapped in some way.
"""

from __future__ import annotations

import pytest
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import SelectionList
from textual.widgets.option_list import Option
from textual.widgets.selection_list import Selection, SelectionError


class SelectionListApp(App[None]):
    """Test selection list application."""

    def compose(self) -> ComposeResult:
        yield SelectionList[int](
            ("0", 0),
            ("1", 1, False),
            ("2", 2, True),
            Selection("3", 3, id="3"),
            Selection("4", 4, True, id="4"),
        )


async def test_options_are_available_soon() -> None:
    """Regression test for https://github.com/Textualize/textual/issues/3903."""

    selection = Selection("", 0, id="some_id")
    selection_list = SelectionList[int](selection)
    assert selection_list.get_option("some_id") is selection


async def test_removing_option_updates_indexes() -> None:
    async with SelectionListApp().run_test() as pilot:
        selections = pilot.app.query_one(SelectionList)
        assert selections._values == {n: n for n in range(5)}

        selections.remove_option_at_index(0)
        assert selections._values == {n + 1: n for n in range(4)}
