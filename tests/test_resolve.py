from fractions import Fraction

import pytest

from textual._resolve import resolve, resolve_fraction_unit
from textual.css.scalar import Scalar
from textual.geometry import Size
from textual.widget import Widget


def test_resolve_fraction_unit_stress_test():
    """Check for zero division errors."""
    # https://github.com/Textualize/textual/issues/2673
    widget = Widget()
    styles = widget.styles
    styles.width = "1fr"

    # We're mainly checking for the absence of zero division errors,
    # which is a reoccurring theme for this code.
    for remaining_space in range(1, 51, 10):
        for max_width in range(1, remaining_space):
            styles.max_width = max_width

            for width in range(1, remaining_space, 2):
                size = Size(width, 24)
                resolved_unit = resolve_fraction_unit(
                    [styles, styles, styles],
                    size,
                    size,
                    Fraction(remaining_space),
                    "width",
                )
                assert resolved_unit <= remaining_space


def test_resolve_issue_2502():
    """Test https://github.com/Textualize/textual/issues/2502"""

    widget = Widget()
    widget.styles.width = "1fr"
    widget.styles.min_width = 11

    assert isinstance(
        resolve_fraction_unit(
            (widget.styles,),
            Size(80, 24),
            Size(80, 24),
            Fraction(10),
            resolve_dimension="width",
        ),
        Fraction,
    )
