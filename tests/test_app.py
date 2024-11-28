import contextlib

from rich.terminal_theme import DIMMED_MONOKAI, MONOKAI, NIGHT_OWLISH

from textual.app import App, ComposeResult
from textual.command import SimpleCommand
from textual.widgets import Button, Input, Static


class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Input()
        yield Button("Click me!")


async def test_search_with_tuples():
    """Test search with a list of tuples and ensure callbacks are invoked.
    In this case we also have no help text in the tuples.
    """
    called = False

    def callback():
        nonlocal called
        called = True

    app = App[None]()
    commands = [
        ("Test Command", callback),
        ("Another Command", callback),
    ]
    async with app.run_test() as pilot:
        await app.search_commands(commands)
        await pilot.press("enter", "enter")
        assert called


async def test_search_with_empty_list():
    """Test search with an empty command list doesn't crash."""
    app = App[None]()
    async with app.run_test() as pilot:
        await app.search_commands([])
        await pilot.press("escape")
