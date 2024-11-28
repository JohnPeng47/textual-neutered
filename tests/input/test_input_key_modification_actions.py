"""Unit tests for Input widget value modification actions."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Input

TEST_INPUTS: dict[str | None, str] = {
    "empty": "",
    "multi-no-punctuation": "Curse your sudden but inevitable betrayal",
    "multi-punctuation": "We have done the impossible, and that makes us mighty.",
    "multi-and-hyphenated": "Long as she does it quiet-like",
}


class InputTester(App[None]):
    """Input widget testing app."""

    def compose(self) -> ComposeResult:
        for input_id, value in TEST_INPUTS.items():
            yield Input(value, id=input_id)


async def test_delete_right_all_from_home() -> None:
    """Deleting all right home should remove everything in the input."""
    async with InputTester().run_test() as pilot:
        for input in pilot.app.query(Input):
            input.cursor_position = 0
            input.action_delete_right_all()
            assert input.cursor_position == 0
            assert input.value == ""


async def test_delete_right_all_from_end() -> None:
    """Deleting all right from end should not change the input's value."""
    async with InputTester().run_test() as pilot:
        for input in pilot.app.query(Input):
            input.action_end()
            input.action_delete_right_all()
            assert input.cursor_position == len(input.value)
            assert input.value == TEST_INPUTS[input.id]
