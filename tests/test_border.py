import pytest
from rich.console import Console
from rich.segment import Segment
from rich.style import Style
from rich.text import Text

from textual._border import render_border_label, render_row
from textual.widget import Widget

_EMPTY_STYLE = Style()
_BLANK_SEGMENT = Segment(" ", _EMPTY_STYLE)
_WIDE_CONSOLE = Console(width=9999)


@pytest.mark.parametrize(
    "label",
    [
        "[b][/]",
        "[i b][/]",
        "[white on red][/]",
        "[blue]",
    ],
)
def test_render_border_empty_text_with_markup(label: str):
    """Test label rendering if there is no text but some markup."""
    assert [] == list(
        render_border_label(
            (Text.from_markup(label), Style()),
            True,
            "round",
            999,
            _EMPTY_STYLE,
            _EMPTY_STYLE,
            _EMPTY_STYLE,
            _WIDE_CONSOLE,
            True,
            True,
        )
    )


def test_render_border_label():
    """Test label rendering with styling, with and without overflow."""

    label = "[b][on red]What [i]is up[/on red] with you?[/]"
    border_style = Style.parse("green on blue")

    # Implicit test on the number of segments returned:
    blank1, what, is_up, with_you, blank2 = render_border_label(
        (Text.from_markup(label), Style()),
        True,
        "round",
        9999,
        _EMPTY_STYLE,
        _EMPTY_STYLE,
        border_style,
        _WIDE_CONSOLE,
        True,
        True,
    )

    expected_blank = Segment(" ", border_style)
    assert blank1 == expected_blank
    assert blank2 == expected_blank

    what_style = Style.parse("b on red")
    expected_what = Segment("What ", border_style + what_style)
    assert what == expected_what

    is_up_style = Style.parse("b on red i")
    expected_is_up = Segment("is up", border_style + is_up_style)
    assert is_up == expected_is_up

    with_you_style = Style.parse("b i")
    expected_with_you = Segment(" with you?", border_style + with_you_style)
    assert with_you == expected_with_you

    blank1, what, blank2 = render_border_label(
        (Text.from_markup(label), Style()),
        True,
        "round",
        5 + 4,  # 5 where "What…" fits + 2 for the blank spaces + 2 for the corners.
        _EMPTY_STYLE,
        _EMPTY_STYLE,
        border_style,
        _WIDE_CONSOLE,
        True,  # This corner costs 2 cells.
        True,  # This corner costs 2 cells.
    )

    assert blank1 == expected_blank
    assert blank2 == expected_blank

    expected_what = Segment("What…", border_style + what_style)
    assert what == expected_what
