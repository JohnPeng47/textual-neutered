"""
Test that generic animations can be disabled.
"""

from textual.app import App, ComposeResult
from textual.color import Color
from textual.widgets import Label


class SingleLabelApp(App[None]):
    """Single label whose background colour we'll animate."""

    CSS = """
        Label {
            background: red;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label()


class LabelWithTransitionsApp(App[None]):
    """Single label whose background is set to animate with TCSS."""

    CSS = """
        Label {
            background: red;
            transition: background 1s;
        }

        Label.blue-bg {
            background: blue;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label()


async def test_style_animations_via_transition_are_disabled_on_basic() -> None:
    app = LabelWithTransitionsApp()
    app.animation_level = "basic"

    async with app.run_test():
        label = app.query_one(Label)
        # Sanity check.
        assert label.styles.background == Color.parse("red")
        animator = app.animator
        # Free time at 0 before triggering the animation.
        animator._get_time = lambda *_: 0
        label.add_class("blue-bg")
        assert len(animator._animations) > 0  # Sanity check.
        # Freeze time after the animation start and before animation end.
        animator._get_time = lambda *_: 0.01
        animator()
        # The animation should have completed.
        assert label.styles.background == Color.parse("blue")


async def test_style_animations_via_transition_are_disabled_on_none() -> None:
    app = LabelWithTransitionsApp()
    app.animation_level = "none"

    async with app.run_test():
        label = app.query_one(Label)
        # Sanity check.
        assert label.styles.background == Color.parse("red")
        animator = app.animator
        # Free time at 0 before triggering the animation.
        animator._get_time = lambda *_: 0
        label.add_class("blue-bg")
        assert len(animator._animations) > 0  # Sanity check.
        # Freeze time after the animation start and before animation end.
        animator._get_time = lambda *_: 0.01
        animator()
        # The animation should have completed.
        assert label.styles.background == Color.parse("blue")
