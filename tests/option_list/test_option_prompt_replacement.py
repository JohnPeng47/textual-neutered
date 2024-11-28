"""Test replacing options prompt from an option list."""

import pytest

from textual.app import App, ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option, OptionDoesNotExist


class OptionListApp(App[None]):
    """Test option list application."""

    def compose(self) -> ComposeResult:
        yield OptionList(
            Option("0", id="0"),
            Option("line1\nline2"),
        )


async def test_replace_multiple_line_option_prompt_with_single() -> None:
    """It should be possible to replace multiple line prompt with a single line"""
    new_prompt = "new-prompt"
    async with OptionListApp().run_test() as pilot:
        option_list = pilot.app.query_one(OptionList)
        option_list.replace_option_prompt("0", new_prompt)
        assert option_list.get_option("0").prompt == new_prompt


async def test_replace_multiple_line_option_prompt_with_multiple() -> None:
    """It should be possible to replace multiple line prompt with multiple lines"""
    new_prompt = "new-prompt\nsecond line"
    async with OptionListApp().run_test() as pilot:
        option_list = pilot.app.query_one(OptionList)
        option_list.replace_option_prompt_at_index(1, new_prompt)
        assert option_list.get_option_at_index(1).prompt == new_prompt
