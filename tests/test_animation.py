from time import perf_counter

from textual.app import App, ComposeResult
from textual.reactive import var
from textual.widgets import Static


class AnimApp(App):
    CSS = """
    #foo {
        height: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("foo", id="foo")


class CancelAnimWidget(Static):
    counter: var[float] = var(23)


class CancelAnimApp(App[None]):
    counter: var[float] = var(23)

    def compose(self) -> ComposeResult:
        yield CancelAnimWidget()


async def test_cancel_widget_animation() -> None:
    """It should be possible to cancel a running widget animation."""

    async with CancelAnimApp().run_test() as pilot:
        widget = pilot.app.query_one(CancelAnimWidget)
        widget.animate("counter", value=0, final_value=1000, duration=60)
        await pilot.pause()
        assert pilot.app.animator.is_being_animated(widget, "counter")
        await widget.stop_animation("counter")
        assert not pilot.app.animator.is_being_animated(widget, "counter")


async def test_cancel_widget_non_animation() -> None:
    """It should be possible to attempt to cancel a non-running widget animation."""

    async with CancelAnimApp().run_test() as pilot:
        widget = pilot.app.query_one(CancelAnimWidget)
        assert not pilot.app.animator.is_being_animated(widget, "counter")
        await widget.stop_animation("counter")
        assert not pilot.app.animator.is_being_animated(widget, "counter")
