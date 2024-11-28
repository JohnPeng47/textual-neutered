from decimal import Decimal

import pytest
from rich.style import Style

from textual.color import Color
from textual.css.errors import StyleValueError
from textual.css.scalar import Scalar, Unit
from textual.css.styles import RenderStyles, Styles
from textual.dom import DOMNode
from textual.widget import Widget


@pytest.mark.parametrize(
    "size_dimension_input,size_dimension_expected_output",
    [
        # fmt: off
        [None, None],
        [1, Scalar(1, Unit.CELLS, Unit.WIDTH)],
        [1.0, Scalar(1.0, Unit.CELLS, Unit.WIDTH)],
        [1.2, Scalar(1.2, Unit.CELLS, Unit.WIDTH)],
        [1.2e3, Scalar(1200.0, Unit.CELLS, Unit.WIDTH)],
        ["20", Scalar(20, Unit.CELLS, Unit.WIDTH)],
        ["1.4", Scalar(1.4, Unit.CELLS, Unit.WIDTH)],
        [Scalar(100, Unit.CELLS, Unit.WIDTH), Scalar(100, Unit.CELLS, Unit.WIDTH)],
        [Scalar(10.3, Unit.CELLS, Unit.WIDTH), Scalar(10.3, Unit.CELLS, Unit.WIDTH)],
        [Scalar(10.4, Unit.CELLS, Unit.HEIGHT), Scalar(10.4, Unit.CELLS, Unit.HEIGHT)],
        [Scalar(10.5, Unit.PERCENT, Unit.WIDTH), Scalar(10.5, Unit.WIDTH, Unit.WIDTH)],
        [Scalar(10.6, Unit.PERCENT, Unit.PERCENT), Scalar(10.6, Unit.WIDTH, Unit.WIDTH)],
        [Scalar(10.7, Unit.HEIGHT, Unit.PERCENT), Scalar(10.7, Unit.HEIGHT, Unit.PERCENT)],
        # percentage values are normalised to floats and get the WIDTH "percent_unit":
        [Scalar(11, Unit.PERCENT, Unit.HEIGHT), Scalar(11.0, Unit.WIDTH, Unit.WIDTH)],
        # fmt: on
    ],
)
def test_widget_style_size_can_accept_various_data_types_and_normalize_them(
    size_dimension_input, size_dimension_expected_output
):
    widget = Widget()

    widget.styles.width = size_dimension_input
    assert widget.styles.width == size_dimension_expected_output


@pytest.mark.parametrize(
    "size_dimension_input",
    [
        "a",
        "1.4e3",
        3.14j,
        Decimal("3.14"),
        list(),
        tuple(),
        dict(),
    ],
)
def test_widget_style_size_fails_if_data_type_is_not_supported(size_dimension_input):
    widget = Widget()

    with pytest.raises(StyleValueError):
        widget.styles.width = size_dimension_input
