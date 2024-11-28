from typing import Literal

import pytest

from textual.geometry import Offset, Region, Size, Spacing, clamp


@pytest.mark.parametrize(
    ("region1", "region2", "expected"),
    [
        (Region(0, 0, 100, 80), Region(0, 0, 100, 80), Spacing(0, 0, 0, 0)),
        (Region(0, 0, 100, 80), Region(10, 10, 10, 10), Spacing(10, 80, 60, 10)),
    ],
)
def test_get_spacing_between(region1: Region, region2: Region, expected: Spacing):
    spacing = region1.get_spacing_between(region2)
    assert spacing == expected
    assert region1.shrink(spacing) == region2


@pytest.mark.parametrize(
    "constrain_x,constrain_y,margin,region,container,expected",
    [
        # A null-op
        (
            "none",
            "none",
            Spacing.unpack(0),
            Region(0, 0, 10, 10),
            Region(0, 0, 100, 100),
            Region(0, 0, 10, 10),
        ),
        # Negative offset gets moved to 0, 0 + margin
        (
            "inside",
            "inside",
            Spacing.unpack(1),
            Region(-5, -5, 10, 10),
            Region(0, 0, 100, 100),
            Region(1, 1, 10, 10),
        ),
        # Overlapping region gets moved in, with offset
        (
            "inside",
            "inside",
            Spacing.unpack(1),
            Region(95, 95, 10, 10),
            Region(0, 0, 100, 100),
            Region(89, 89, 10, 10),
        ),
        # X coordinate moved inside, region reflected around it's Y axis
        (
            "inside",
            "inflect",
            Spacing.unpack(1),
            Region(-5, -5, 10, 10),
            Region(0, 0, 100, 100),
            Region(1, 6, 10, 10),
        ),
    ],
)
def test_constrain(
    constrain_x: Literal["none", "inside", "inflect"],
    constrain_y: Literal["none", "inside", "inflect"],
    margin: Spacing,
    region: Region,
    container: Region,
    expected: Region,
) -> None:
    assert region.constrain(constrain_x, constrain_y, margin, container) == expected
