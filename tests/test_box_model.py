from __future__ import annotations

from fractions import Fraction

from textual.box_model import BoxModel
from textual.geometry import Size, Spacing
from textual.widget import Widget


def test_max():
    """Check that max_width and max_height are respected."""
    one = Fraction(1)

    class TestWidget(Widget):
        def get_content_width(self, container: Size, parent: Size) -> int:
            assert False, "must not be called"

        def get_content_height(self, container: Size, parent: Size, width: int) -> int:
            assert False, "must not be called"

    widget = TestWidget()
    styles = widget.styles

    styles.width = 100
    styles.height = 80
    styles.max_width = 40
    styles.max_height = 30

    box_model = widget._get_box_model(Size(40, 30), Size(80, 24), one, one)
    assert box_model == BoxModel(Fraction(40), Fraction(30), Spacing(0, 0, 0, 0))


def test_min():
    """Check that min_width and min_height are respected."""

    one = Fraction(1)

    class TestWidget(Widget):
        def get_content_width(self, container: Size, parent: Size) -> int:
            assert False, "must not be called"

        def get_content_height(self, container: Size, parent: Size, width: int) -> int:
            assert False, "must not be called"

    widget = TestWidget()
    styles = widget.styles
    styles.width = 10
    styles.height = 5
    styles.min_width = 40
    styles.min_height = 30

    box_model = widget._get_box_model(Size(40, 30), Size(80, 24), one, one)
    assert box_model == BoxModel(Fraction(40), Fraction(30), Spacing(0, 0, 0, 0))
