from textual.app import App, ComposeResult
from textual.color import Color
from textual.containers import Container
from textual.css.scalar import ScalarOffset


class StyleApp(App[None]):
    CSS = """
    Container {
        border: round green !important;
        outline: round green !important;
        align: right bottom !important;
        content-align: right bottom !important;
        offset: 17 23 !important;
        overflow: hidden hidden !important;
        padding: 10 20 30 40 !important;
        scrollbar-size: 23 42 !important;
    }

    Container.more-specific {
        border: solid red;
        outline: solid red;
        align: center middle;
        content-align: center middle;
        offset: 0 0;
        overflow: scroll scroll;
        padding: 1 2 3 4;
        scrollbar-size: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Container(classes="more-specific")


async def test_padding_importance():
    """Padding without sides should support !important"""
    async with StyleApp().run_test() as pilot:
        padding = pilot.app.query_one(Container).styles.padding
        assert padding.top == 10
        assert padding.left == 40
        assert padding.bottom == 30
        assert padding.right == 20


async def test_scrollbar_size_importance():
    """Scrollbar size without direction should support !important"""
    async with StyleApp().run_test() as pilot:
        assert pilot.app.query_one(Container).styles.scrollbar_size_horizontal == 23
        assert pilot.app.query_one(Container).styles.scrollbar_size_vertical == 42
