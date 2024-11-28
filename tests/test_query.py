import pytest

from textual.app import App, ComposeResult
from textual.color import Color
from textual.containers import Container
from textual.css.query import (
    DeclarationError,
    InvalidQueryFormat,
    NoMatches,
    TooManyMatches,
    WrongType,
)
from textual.widget import Widget
from textual.widgets import Input, Label


@pytest.mark.parametrize(
    "args", [(False, False), (True, False), (True, True), (False, True)]
)
async def test_query_refresh(args):
    refreshes = []

    class MyWidget(Widget):
        def refresh(self, *, repaint=None, layout=None, recompose=None):
            super().refresh(repaint=repaint, layout=layout)
            refreshes.append((repaint, layout))

    class MyApp(App):
        def compose(self):
            yield MyWidget()

    app = MyApp()
    async with app.run_test() as pilot:
        app.query(MyWidget).refresh(repaint=args[0], layout=args[1])
        assert refreshes[-1] == args


async def test_query_focus_blur():
    class FocusApp(App):
        AUTO_FOCUS = None

        def compose(self) -> ComposeResult:
            yield Input(id="foo")
            yield Input(id="bar")
            yield Input(id="baz")

    app = FocusApp()
    async with app.run_test() as pilot:
        # Nothing focused
        assert app.focused is None
        # Focus first input
        app.query(Input).focus()
        await pilot.pause()
        assert app.focused.id == "foo"
        # Blur inputs
        app.query(Input).blur()
        await pilot.pause()
        assert app.focused is None
        # Focus another
        app.query("#bar").focus()
        await pilot.pause()
        assert app.focused.id == "bar"
        # Focus non existing
        app.query("#egg").focus()
        assert app.focused.id == "bar"
