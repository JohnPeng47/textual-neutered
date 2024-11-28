"""Unit tests for Input widget position movement actions."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Input


class InputTester(App[None]):
    """Input widget testing app."""

    def compose(self) -> ComposeResult:
        for value, input_id in (
            ("", "empty"),
            ("Shiny", "single-word"),
            ("Curse your sudden but inevitable betrayal", "multi-no-punctuation"),
            (
                "We have done the impossible, and that makes us mighty.",
                "multi-punctuation",
            ),
            ("Long as she does it quiet-like", "multi-and-hyphenated"),
        ):
            yield Input(value, id=input_id)


async def test_input_right_word_to_the_end() -> None:
    """Using right-word to get to the end should hop the correct number of times."""
    async with InputTester().run_test() as pilot:
        expected_hops: dict[str | None, int] = {
            "empty": 0,
            "single-word": 1,
            "multi-no-punctuation": 6,
            "multi-punctuation": 10,
            "multi-and-hyphenated": 7,
        }
        for input in pilot.app.query(Input):
            input.cursor_position = 0
            hops = 0
            while input.cursor_position < len(input.value):
                input.action_cursor_right_word()
                hops += 1
            assert hops == expected_hops[input.id]


async def test_input_left_word_from_the_end() -> None:
    """Using left-word to get home from the end should hop the correct number of times."""
    async with InputTester().run_test() as pilot:
        expected_hops: dict[str | None, int] = {
            "empty": 0,
            "single-word": 1,
            "multi-no-punctuation": 6,
            "multi-punctuation": 10,
            "multi-and-hyphenated": 7,
        }
        for input in pilot.app.query(Input):
            input.action_end()
            hops = 0
            while input.cursor_position:
                input.action_cursor_left_word()
                hops += 1
            assert hops == expected_hops[input.id]


# TODO: more tests.
