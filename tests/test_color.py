import pytest
from rich.color import Color as RichColor

from textual.color import Color, Gradient, Lab, lab_to_rgb, rgb_to_lab


# Computed with http://www.easyrgb.com/en/convert.php,
# (r, g, b) values in sRGB to (L*, a*, b*) values in CIE-L*ab.
RGB_LAB_DATA = [
    (10, 23, 73, 10.245, 15.913, -32.672),
    (200, 34, 123, 45.438, 67.750, -8.008),
    (0, 0, 0, 0, 0, 0),
    (255, 255, 255, 100, 0, 0),
]


def test_is_transparent():
    """Check is_transparent is reporting correctly."""
    assert Color(0, 0, 0, 0).is_transparent
    assert Color(20, 20, 30, 0).is_transparent
    assert not Color(20, 20, 30, a=0.01).is_transparent
    assert not Color(20, 20, 30, a=1).is_transparent
    assert not Color(20, 20, 30, 0, ansi=1).is_transparent


@pytest.mark.parametrize(
    "base,tint,expected",
    [
        (
            Color(0, 0, 0),
            Color(10, 20, 30),
            Color(10, 20, 30),
        ),
        (
            Color(0, 0, 0, 0.5),
            Color(255, 255, 255, 0.5),
            Color(127, 127, 127, 0.5),
        ),
        (
            Color(100, 0, 0, 0.2),
            Color(0, 100, 0, 0.5),
            Color(50, 50, 0, 0.2),
        ),
        (Color(10, 20, 30), Color.parse("ansi_red"), Color(10, 20, 30)),
    ],
)
def test_tint(base: Color, tint: Color, expected: Color) -> None:
    assert base.tint(tint) == expected
