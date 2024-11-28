"""Core option list unit tests, aimed at testing basic list creation."""

from __future__ import annotations

import pytest

from textual.app import App, ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import (
    DuplicateID,
    Option,
    OptionDoesNotExist,
    Separator,
)


class OptionListApp(App[None]):
    """Test option list application."""

    def compose(self) -> ComposeResult:
        yield OptionList(
            "0",
            Option("1"),
            Separator(),
            Option("2", disabled=True),
            None,
            Option("3", id="3"),
            Option("4", id="4", disabled=True),
        )


async def test_adding_multiple_duplicates_at_once() -> None:
    """Adding duplicates together than aren't existing duplicates should be an error."""
    async with OptionListApp().run_test() as pilot:
        option_list = pilot.app.query_one(OptionList)
        assert option_list.option_count == 5
        with pytest.raises(DuplicateID):
            option_list.add_options(
                [
                    Option("dupe", id="42"),
                    Option("dupe", id="42"),
                ]
            )
        assert option_list.option_count == 5


async def test_options_are_available_soon() -> None:
    """Regression test for https://github.com/Textualize/textual/issues/3903."""

    option = Option("", id="some_id")
    option_list = OptionList(option)
    assert option_list.get_option("some_id") is option
