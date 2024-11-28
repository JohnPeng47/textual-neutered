import pytest
from rich.segment import Segment
from rich.style import Style

from textual._segment_tools import NoCellPositionForIndex
from textual.color import Color
from textual.filter import Monochrome
from textual.strip import Strip


def test_index_cell_position_index_too_large():
    strip = Strip([Segment("abcdef"), Segment("ghi")])
    with pytest.raises(NoCellPositionForIndex):
        strip.index_to_cell_position(100)


def test_text():
    assert Strip([]).text == ""
    assert Strip([Segment("foo")]).text == "foo"
    assert Strip([Segment("foo"), Segment("bar")]).text == "foobar"
