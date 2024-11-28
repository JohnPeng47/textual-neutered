from string import punctuation

import pytest

from textual import events, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle
from textual.css.errors import StylesheetError
from textual.pilot import OutOfBounds
from textual.screen import Screen
from textual.widgets import Button, Label
from textual.worker import WorkerFailed

KEY_CHARACTERS_TO_TEST = "akTW03" + punctuation
"""Test some "simple" characters (letters + digits) and all punctuation."""


class CenteredButtonApp(App):
    CSS = """  # Ensure the button is 16 x 3
    Button {
        min-width: 16;
        max-width: 16;
        width: 16;
        min-height: 3;
        max-height: 3;
        height: 3;
    }
    """

    def compose(self):
        with Center():
            with Middle():
                yield Button()


class ManyLabelsApp(App):
    """Auxiliary app with a button following many labels."""

    AUTO_FOCUS = None  # So that there's no auto-scrolling.

    def compose(self):
        for idx in range(100):
            yield Label(f"label {idx}", id=f"label{idx}")
        yield Button()


async def test_fail_early():
    # https://github.com/Textualize/textual/issues/3282
    class MyApp(App):
        CSS_PATH = "foo.tcss"

    app = MyApp()
    with pytest.raises(StylesheetError):
        async with app.run_test() as pilot:
            await pilot.press("enter")


async def test_click_by_widget():
    """Test that click accept a Widget instance."""
    pressed = False

    class TestApp(CenteredButtonApp):
        def on_button_pressed(self):
            nonlocal pressed
            pressed = True

    app = TestApp()
    async with app.run_test() as pilot:
        button = app.query_one(Button)
        assert not pressed
        await pilot.click(button)
        assert pressed
