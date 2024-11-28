from __future__ import annotations

import pytest

from textual._widget_navigation import (
    find_first_enabled,
    find_last_enabled,
    find_next_enabled,
    find_next_enabled_no_wrap,
    get_directed_distance,
)


class _D:
    def __init__(self, disabled):
        self.disabled = disabled


# Represent disabled/enabled objects that are compact to write in tests.
D = _D(True)
E = _D(False)


@pytest.mark.parametrize(
    ["candidates", "anchor", "direction", "result"],
    [
        # No anchor & no candidates -> no next
        ([], None, 1, None),
        ([], None, -1, None),
        # No anchor but candidates -> get first/last one
        ([E], None, 1, 0),
        ([E, D], None, 1, 0),
        ([E, E], None, 1, 0),
        ([D, E], None, 1, 1),
        ([D, D, E], None, 1, 2),
        ([E], None, -1, 0),
        ([E, E], None, -1, 1),
        ([E, D], None, -1, 0),
        ([E, D, D], None, -1, 0),
        # No enabled candidates -> return None
        ([D, D, D], 0, 1, None),
        ([D, D, D], 1, 1, None),
        ([D, D, D], 1, -1, None),
        ([D, D, D], None, -1, None),
        # General case
        # 0  1  2  3  4  5
        ([E, D, D, E, E, D], 0, 1, 3),
        ([E, D, D, E, E, D], 0, -1, None),
        ([E, D, D, E, E, D], 1, 1, 3),
        ([E, D, D, E, E, D], 1, -1, 0),
        ([E, D, D, E, E, D], 2, 1, 3),
        ([E, D, D, E, E, D], 2, -1, 0),
        ([E, D, D, E, E, D], 3, 1, 4),
        ([E, D, D, E, E, D], 3, -1, 0),
        ([E, D, D, E, E, D], 4, 1, None),
        ([E, D, D, E, E, D], 4, -1, 3),
        ([E, D, D, E, E, D], 5, 1, None),
        ([E, D, D, E, E, D], 5, -1, 4),
    ],
)
def test_find_next_enabled_no_wrap(candidates, anchor, direction, result):
    assert find_next_enabled_no_wrap(candidates, anchor, direction) == result


@pytest.mark.parametrize(
    ["function", "start", "direction"],
    [
        (find_next_enabled_no_wrap, 0, 1),
        (find_next_enabled_no_wrap, 0, -1),
        (find_next_enabled_no_wrap, 1, 1),
        (find_next_enabled_no_wrap, 1, -1),
        (find_next_enabled_no_wrap, 2, 1),
        (find_next_enabled_no_wrap, 2, -1),
    ],
)
def test_find_next_with_anchor(function, start, direction):
    assert function([E, E, E], start, direction, True) == start
