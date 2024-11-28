import pytest

from textual.app import App, ComposeResult
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Label


class Focusable(Widget, can_focus=True):
    pass


class NonFocusable(Widget, can_focus=False, can_focus_children=False):
    pass


class ChildrenFocusableOnly(Widget, can_focus=False, can_focus_children=True):
    pass


@pytest.fixture
def screen() -> Screen:
    app = App()

    with app._context():
        app.push_screen(Screen())

        screen = app.screen

        # The classes even/odd alternate along the focus chain.
        # The classes in/out identify nested widgets.
        screen._add_children(
            Focusable(id="foo", classes="a"),
            NonFocusable(id="bar"),
            Focusable(Focusable(id="Paul", classes="c"), id="container1", classes="b"),
            NonFocusable(Focusable(id="Jessica", classes="a"), id="container2"),
            Focusable(id="baz", classes="b"),
            ChildrenFocusableOnly(Focusable(id="child", classes="c")),
        )

        return screen


async def test_focus_pseudo_class():
    """Test focus and blue pseudo classes"""

    # https://github.com/Textualize/textual/pull/3645
    class FocusApp(App):
        AUTO_FOCUS = None

        def compose(self) -> ComposeResult:
            yield Button("Hello")

    app = FocusApp()
    async with app.run_test() as pilot:
        button = app.query_one(Button)
        classes = list(button.get_pseudo_classes())
        # Blurred, not focused
        assert "blur" in classes
        assert "focus" not in classes

        # Focus the button
        button.focus()
        await pilot.pause()

        # Focused, not blurred
        classes = list(button.get_pseudo_classes())
        assert "blur" not in classes
        assert "focus" in classes


async def test_get_focusable_widget_at() -> None:
    """Check that clicking a non-focusable widget will focus any (focusable) ancestors."""

    class FocusApp(App):
        AUTO_FOCUS = None

        def compose(self) -> ComposeResult:
            with ScrollableContainer(id="focusable"):
                with Container():
                    yield Label("Foo", id="foo")
                    yield Label("Bar", id="bar")
            yield Label("Egg", id="egg")

    app = FocusApp()
    async with app.run_test() as pilot:
        # Nothing focused
        assert app.screen.focused is None
        # Click foo
        await pilot.click("#foo")
        # Confirm container is focused
        assert app.screen.focused is not None
        assert app.screen.focused.id == "focusable"
        # Reset focus
        app.screen.set_focus(None)
        assert app.screen.focused is None
        # Click bar
        await pilot.click("#bar")
        # Confirm container is focused
        assert app.screen.focused is not None
        assert app.screen.focused.id == "focusable"
        # Reset focus
        app.screen.set_focus(None)
        assert app.screen.focused is None
        # Click egg (outside of focusable widget)
        await pilot.click("#egg")
        # Confirm nothing focused
        assert app.screen.focused is None
