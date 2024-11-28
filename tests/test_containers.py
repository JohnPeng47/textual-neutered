"""Test basic functioning of some containers."""

from textual.app import App, ComposeResult
from textual.containers import (
    Center,
    Horizontal,
    HorizontalScroll,
    Middle,
    Vertical,
    VerticalScroll,
)
from textual.widgets import Label


async def test_middle_container():
    """Check the size of the container `Middle`."""

    class MiddleApp(App[None]):
        def compose(self) -> ComposeResult:
            with Middle():
                yield Label("1234")

    app = MiddleApp()
    async with app.run_test():
        middle = app.query_one(Middle)
        assert middle.size.width == 4
        assert middle.size.height == app.size.height


async def test_scrollbar_zero_thickness():
    """Ensuring that scrollbars can be set to zero thickness."""

    class ScrollbarZero(App):
        CSS = """* {
            scrollbar-size: 0 0;
            scrollbar-size-vertical: 0;  /* just exercising the parser */
            scrollbar-size-horizontal: 0;  /* exercise the parser */
        }
        """

        def compose(self) -> ComposeResult:
            with Vertical():
                for _ in range(10):
                    yield Label("Hello, world!")

    app = ScrollbarZero()
    async with app.run_test(size=(8, 6)):
        pass
