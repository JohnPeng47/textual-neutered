from collections import UserList, deque
from typing import Sequence

import pytest

from tests.utilities.render import render
from textual.renderables.sparkline import Sparkline

GREEN = "\x1b[38;2;0;255;0m"
RED = "\x1b[38;2;255;0;0m"
BLENDED = "\x1b[38;2;127;127;0m"  # Color between red and green
STOP = "\x1b[0m"


def test_sparkline_color_blend():
    assert (
        render(Sparkline([1, 2, 3], width=3))
        == f"{GREEN}▁{STOP}{BLENDED}▄{STOP}{RED}█{STOP}"
    )


@pytest.mark.parametrize(
    "data",
    [
        (1, 2, 3),
        [1, 2, 3],
        bytearray((1, 2, 3)),
        bytes((1, 2, 3)),
        deque([1, 2, 3]),
        range(1, 4),
        UserList((1, 2, 3)),
    ],
)
def test_sparkline_sequence_types(data: Sequence[int]):
    """Sparkline should work with common Sequence types."""
    assert issubclass(type(data), Sequence)
    assert (
        render(Sparkline(data, width=3))
        == f"{GREEN}▁{STOP}{BLENDED}▄{STOP}{RED}█{STOP}"
    )
