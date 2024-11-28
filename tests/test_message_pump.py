import pytest

from textual._dispatch_key import dispatch_key
from textual.app import App, ComposeResult
from textual.errors import DuplicateKeyHandlers
from textual.events import Key
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Input, Label


class ValidWidget(Widget):
    called_by = None

    def key_x(self):
        self.called_by = self.key_x

    def key_ctrl_i(self):
        self.called_by = self.key_ctrl_i


class DuplicateHandlersWidget(Widget):
    called_by = None

    def key_x(self):
        self.called_by = self.key_x

    def _key_x(self):
        self.called_by = self._key_x

    def key_tab(self):
        self.called_by = self.key_tab

    def key_ctrl_i(self):
        self.called_by = self.key_ctrl_i


class PreventTestApp(App):
    def __init__(self) -> None:
        self.input_changed_events = []
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Input()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.input_changed_events.append(event)


async def test_prevent_with_call_next() -> None:
    """Test for https://github.com/Textualize/textual/issues/3166.

    Does a callback scheduled with `call_next` respect messages that
    were prevented when it was scheduled?
    """

    hits = 0

    class PreventTestApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Input()

        def change_input(self) -> None:
            self.query_one(Input).value += "a"

        def on_input_changed(self) -> None:
            nonlocal hits
            hits += 1

    app = PreventTestApp()
    async with app.run_test() as pilot:
        app.call_next(app.change_input)
        await pilot.pause()
        assert hits == 1

        with app.prevent(Input.Changed):
            app.call_next(app.change_input)
        await pilot.pause()
        assert hits == 1

        app.call_next(app.change_input)
        await pilot.pause()
        assert hits == 2


async def test_prevent_default():
    """Test that prevent_default doesn't apply when a message is bubbled."""

    app_button_pressed = False

    class MyButton(Button):
        def _on_button_pressed(self, event: Button.Pressed) -> None:
            event.prevent_default()

    class PreventApp(App[None]):
        def compose(self) -> ComposeResult:
            yield MyButton("Press me")
            yield Label("No pressure")

        def on_button_pressed(self, event: Button.Pressed) -> None:
            nonlocal app_button_pressed
            app_button_pressed = True
            self.query_one(Label).update("Ouch!")

    app = PreventApp()
    async with app.run_test() as pilot:
        await pilot.click(MyButton)
        assert app_button_pressed
