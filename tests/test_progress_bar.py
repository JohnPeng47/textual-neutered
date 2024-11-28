import pytest
from pytest import approx
from rich.console import Console
from rich.text import Text

from textual.app import App
from textual.color import Gradient
from textual.css.query import NoMatches
from textual.renderables.bar import _apply_gradient
from textual.widget import Widget
from textual.widgets import ProgressBar


@pytest.mark.parametrize(
    ["show_bar", "show_percentage", "show_eta"],
    [
        (True, True, True),
        (True, True, False),
        (True, False, True),
        (True, False, False),
        (False, True, True),
        (False, True, False),
        (False, False, True),
        (False, False, False),
    ],
)
async def test_show_sub_widgets(show_bar: bool, show_percentage: bool, show_eta: bool):
    class PBApp(App[None]):
        def compose(self):
            self.pb = ProgressBar(
                show_bar=show_bar, show_percentage=show_percentage, show_eta=show_eta
            )
            yield self.pb

    app = PBApp()

    async with app.run_test():
        if show_bar:
            bar = app.pb.query_one("#bar")
            assert isinstance(bar, Widget)
        else:
            with pytest.raises(NoMatches):
                app.pb.query_one("#bar")

        if show_percentage:
            percentage = app.pb.query_one("#percentage")
            assert isinstance(percentage, Widget)
        else:
            with pytest.raises(NoMatches):
                app.pb.query_one("#percentage")

        if show_eta:
            eta = app.pb.query_one("#eta")
            assert isinstance(eta, Widget)
        else:
            with pytest.raises(NoMatches):
                app.pb.query_one("#eta")


def test_apply_gradient():
    text = Text("foo")
    gradient = Gradient.from_colors("red", "blue")
    _apply_gradient(text, gradient, 1)
    console = Console()
    assert text.get_style_at_offset(console, 0).color.triplet == (255, 0, 0)
