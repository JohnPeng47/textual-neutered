"""Test movement within an option list."""

from __future__ import annotations

import pytest

from textual.app import App, ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option


class OptionListApp(App[None]):
    """Test option list application."""

    def compose(self) -> ComposeResult:
        yield OptionList("1", "2", "3", None, "4", "5", "6")


class EmptyOptionListApp(App[None]):
    """Test option list application with no optons."""

    def compose(self) -> ComposeResult:
        yield OptionList()


@pytest.mark.parametrize(
    ["movement", "landing"],
    [
        ("up", 99),
        ("down", 0),
        ("home", 0),
        ("end", 99),
        ("pageup", 0),
        ("pagedown", 99),
    ],
)
async def test_no_highlight_movement(movement: str, landing: int) -> None:
    """Attempting to move around in a list with no highlight should select the most appropriate item."""
    async with EmptyOptionListApp().run_test() as pilot:
        option_list = pilot.app.query_one(OptionList)
        for _ in range(100):
            option_list.add_option("test")
        await pilot.press("tab")
        await pilot.press(movement)
        assert option_list.highlighted == landing


class OptionListDisabledOptionsApp(App[None]):
    def compose(self) -> ComposeResult:
        self.highlighted = []
        yield OptionList(
            Option("0", disabled=True),
            Option("1"),
            Option("2", disabled=True),
            Option("3", disabled=True),
            Option("4"),
            Option("5"),
            Option("6", disabled=True),
            Option("7"),
            Option("8", disabled=True),
        )

    def _on_option_list_option_highlighted(
        self, message: OptionList.OptionHighlighted
    ) -> None:
        self.highlighted.append(str(message.option.prompt))


async def test_keyboard_navigation_with_disabled_options() -> None:
    """Regression test for https://github.com/Textualize/textual/issues/3881."""

    app = OptionListDisabledOptionsApp()
    async with app.run_test() as pilot:
        for _ in range(5):
            await pilot.press("down")
        for _ in range(5):
            await pilot.press("up")

    assert app.highlighted == [
        "1",
        "4",
        "5",
        "7",
        "1",
        "4",
        "1",
        "7",
        "5",
        "4",
        "1",
    ]
