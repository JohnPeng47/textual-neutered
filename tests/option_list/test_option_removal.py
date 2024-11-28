"""Test removing options from an option list."""

from __future__ import annotations

import pytest

from textual.app import App, ComposeResult
from textual.geometry import Offset
from textual.widgets import OptionList
from textual.widgets.option_list import Option, OptionDoesNotExist


class OptionListApp(App[None]):
    """Test option list application."""

    def compose(self) -> ComposeResult:
        yield OptionList(
            Option("0", id="0"),
            Option("1", id="1"),
        )


async def test_remove_invalid_index() -> None:
    """Attempting to remove an option index that doesn't exist should raise an exception."""
    async with OptionListApp().run_test() as pilot:
        with pytest.raises(OptionDoesNotExist):
            pilot.app.query_one(OptionList).remove_option_at_index(23)


async def test_remove_with_hover_on_last_option():
    """https://github.com/Textualize/textual/issues/3270"""
    async with OptionListApp().run_test() as pilot:
        await pilot.hover(OptionList, Offset(1, 1) + Offset(2, 1))
        option_list = pilot.app.query_one(OptionList)
        assert option_list._mouse_hovering_over == 1
        option_list.remove_option_at_index(0)
        assert option_list._mouse_hovering_over == None
