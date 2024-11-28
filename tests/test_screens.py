from __future__ import annotations

import asyncio
import sys
import threading

import pytest

from textual import work
from textual.app import App, ComposeResult, ScreenStackError
from textual.events import MouseMove
from textual.geometry import Offset
from textual.screen import Screen
from textual.widgets import Button, Input, Label
from textual.worker import NoActiveWorker

skip_py310 = pytest.mark.skipif(
    sys.version_info.minor == 10 and sys.version_info.major == 3,
    reason="segfault on py3.10",
)


async def test_worker_cancellation():
    """Regression test for https://github.com/Textualize/textual/issues/4884

    The MRE below was pushing a screen in an exclusive worker.
    This was previously breaking because the second time the worker was launched,
    it cancelled the first one which was awaiting the screen.

    """
    from textual import on, work
    from textual.app import App
    from textual.containers import Vertical
    from textual.screen import Screen
    from textual.widgets import Button, Footer, Label

    class InfoScreen(Screen[bool]):
        def __init__(self, question: str) -> None:
            self.question = question
            super().__init__()

        def compose(self) -> ComposeResult:
            yield Vertical(
                Label(self.question, id="info-label"),
                Button("Ok", variant="primary", id="ok"),
                id="info-vertical",
            )
            yield Footer()

        @on(Button.Pressed, "#ok")
        def handle_ok(self) -> None:
            self.dismiss(True)  # Changed the `dismiss` result to compatible type

    class ExampleApp(App):
        BINDINGS = [("i", "info", "Info")]

        screen_count = 0

        def compose(self) -> ComposeResult:
            yield Label("This is the default screen")
            yield Footer()

        @work(exclusive=True)
        async def action_info(self) -> None:
            # Since this is an exclusive worker, the second time it is called,
            # the original `push_screen_wait` is also cancelled
            self.screen_count += 1
            await self.push_screen_wait(
                InfoScreen(f"This is info screen #{self.screen_count}")
            )

    app = ExampleApp()
    async with app.run_test() as pilot:
        # Press i twice to launch 2 InfoScreens
        await pilot.press("i")
        await pilot.press("i")
        # Press enter to activate button to dismiss them
        await pilot.press("enter")
        await pilot.press("enter")


async def test_get_screen_with_expected_type():
    """Test get_screen with expected type works"""

    class BadScreen(Screen[None]):
        pass

    class MyScreen(Screen[None]):
        def compose(self):
            yield Label()
            yield Button()

    class MyApp(App[None]):
        SCREENS = {"my_screen": MyScreen}

        def on_mount(self):
            self.push_screen("my_screen")

    app = MyApp()
    async with app.run_test():
        screen = app.get_screen("my_screen")
        # Should be fine
        assert isinstance(screen, MyScreen)

        screen = app.get_screen("my_screen", MyScreen)
        # Should be fine
        assert isinstance(screen, MyScreen)

        # TypeError because my_screen is not a BadScreen
        with pytest.raises(TypeError):
            screen = app.get_screen("my_screen", BadScreen)
