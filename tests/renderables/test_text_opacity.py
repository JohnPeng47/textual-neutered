import pytest
from rich.text import Text

from tests.utilities.render import render
from textual.renderables.text_opacity import TextOpacity

STOP = "\x1b[0m"


@pytest.fixture
def text():
    return Text("Hello, world!", style="#ff0000 on #00ff00", end="")


def test_text_opacity_only_fg_noop():
    text_only_fg = Text("Hello, world!", style="#ff0000", end="")
    assert render(TextOpacity(text_only_fg, opacity=0.5)) == render(text_only_fg)


def test_text_opacity_only_bg_noop():
    text_only_bg = Text("Hello, world!", style="on #ff0000", end="")
    assert render(TextOpacity(text_only_bg, opacity=0.5)) == render(text_only_bg)
