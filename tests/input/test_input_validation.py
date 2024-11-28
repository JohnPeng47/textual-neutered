import pytest

from textual import on
from textual.app import App, ComposeResult
from textual.validation import Number, ValidationResult
from textual.widgets import Input


class InputApp(App):
    def __init__(self, validate_on=None):
        super().__init__()
        self.messages = []
        self.validator = Number(minimum=1, maximum=5)
        self.validate_on = validate_on

    def compose(self) -> ComposeResult:
        yield Input(
            validators=self.validator,
            validate_on=self.validate_on,
        )

    @on(Input.Changed)
    @on(Input.Submitted)
    def on_changed_or_submitted(self, event):
        self.messages.append(event)


async def test_none_validate_on_means_all_validations_happen():
    app = InputApp(None)
    async with app.run_test() as pilot:
        assert len(app.messages) == 0  # sanity checks
        input = app.query_one(Input)
        assert not input.has_class("-valid")
        assert not input.has_class("-invalid")

        input.value = "3"
        await pilot.pause()
        assert len(app.messages) == 1
        assert app.messages[-1].validation_result is not None
        assert input.has_class("-valid")

        input.remove_class("-valid")

        await input.action_submit()
        await pilot.pause()
        assert len(app.messages) == 2
        assert app.messages[-1].validation_result is not None
        assert input.has_class("-valid")

        input.remove_class("-valid")

        input.focus()
        await pilot.pause()
        app.set_focus(None)
        await pilot.pause()
        assert input.has_class("-valid")


async def test_valid_empty():
    app = InputApp(None)
    async with app.run_test() as pilot:
        input = app.query_one(Input)

        await pilot.press("1", "backspace")

        assert not input.has_class("-valid")
        assert input.has_class("-invalid")

        input.valid_empty = True

        assert input.has_class("-valid")
        assert not input.has_class("-invalid")
