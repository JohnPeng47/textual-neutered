import re

import pytest

from textual.app import App, ComposeResult
from textual.widgets import Input
from textual.widgets._input import _RESTRICT_TYPES


async def test_restrict():
    """Test restriction by regex."""

    class InputApp(App):
        AUTO_FOCUS = "Input"

        def compose(self) -> ComposeResult:
            yield Input(restrict="[abc]*")

    async with InputApp().run_test() as pilot:
        input_widget = pilot.app.query_one(Input)
        await pilot.press("a")
        assert input_widget.value == "a"
        await pilot.press("b")
        assert input_widget.value == "ab"
        await pilot.press("c")
        assert input_widget.value == "abc"
        # "d" is restricted
        await pilot.press("d")
        assert input_widget.value == "abc"
        # "a" is not
        await pilot.press("a")
        assert input_widget.value == "abca"


async def test_restrict_type():
    class InputApp(App):
        def compose(self) -> ComposeResult:
            yield Input(type="integer", id="integer")
            yield Input(type="number", id="number")
            yield Input(type="text", id="text")

    async with InputApp().run_test() as pilot:
        integer_input = pilot.app.query_one("#integer", Input)
        number_input = pilot.app.query_one("#number", Input)
        text_input = pilot.app.query_one("#text", Input)

        integer_input.focus()
        await pilot.press("a")
        assert not integer_input.value
        await pilot.press("-")
        assert integer_input.value == "-"
        assert integer_input.is_valid is False

        await pilot.press("1")
        assert integer_input.value == "-1"
        assert integer_input.is_valid is True

        number_input.focus()
        await pilot.press("x")
        assert number_input.value == ""
        await pilot.press("-", "3", ".", "1", "4", "y")
        assert number_input.value == "-3.14"

        text_input.focus()
        await pilot.press("!", "x", "9")
        assert text_input.value == "!x9"
