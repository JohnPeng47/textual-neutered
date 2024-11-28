from rich.segment import Segment
from rich.style import Style

from textual._segment_tools import align_lines, line_crop, line_pad, line_trim
from textual.geometry import Size


def test_align_lines_perfect_fit_horizontal_center():
    """When the content perfectly fits the available horizontal space,
    no empty segments should be produced. This is a regression test for
    the issue https://github.com/Textualize/textual/issues/3628."""
    lines = [[Segment("  "), Segment("hello"), Segment("   ")]]  # 10 cells of content
    result = align_lines(
        lines, Style(), size=Size(10, 1), horizontal="center", vertical="middle"
    )
    assert list(result) == [[Segment("  "), Segment("hello"), Segment("   ")]]


def test_align_lines_perfect_fit_horizontal_right():
    """When the content perfectly fits the available horizontal space,
    no empty segments should be produced. This is a regression test for
    the issue https://github.com/Textualize/textual/issues/3628."""
    lines = [[Segment("  "), Segment("hello"), Segment("   ")]]  # 10 cells of content
    result = align_lines(
        lines, Style(), size=Size(10, 1), horizontal="right", vertical="middle"
    )
    assert list(result) == [[Segment("  "), Segment("hello"), Segment("   ")]]
