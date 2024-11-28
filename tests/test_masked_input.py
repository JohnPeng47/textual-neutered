from typing import Union

import pytest

from textual import on
from textual.app import App, ComposeResult
from textual.validation import Failure, ValidationResult
from textual.widgets import MaskedInput

InputEvent = Union[MaskedInput.Changed, MaskedInput.Submitted]


class InputApp(App[None]):
    def __init__(self, template: str, placeholder: str = ""):
        super().__init__()
        self.messages: list[InputEvent] = []
        self.template = template
        self.placeholder = placeholder

    def compose(self) -> ComposeResult:
        yield MaskedInput(template=self.template, placeholder=self.placeholder)

    @on(MaskedInput.Changed)
    @on(MaskedInput.Submitted)
    def on_changed_or_submitted(self, event: InputEvent) -> None:
        self.messages.append(event)


async def test_digits_not_required():
    app = InputApp("00;_")
    async with app.run_test() as pilot:
        input = app.query_one(MaskedInput)
        await pilot.press("a", "1")
        assert input.value == "1"
        assert input.is_valid


async def test_digits_required():
    app = InputApp("99;_")
    async with app.run_test() as pilot:
        input = app.query_one(MaskedInput)
        await pilot.press("a", "1")
        assert input.value == "1"
        assert not input.is_valid
