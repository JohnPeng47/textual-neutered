from typing import Sequence

import pytest

from textual._immutable_sequence_view import ImmutableSequenceView


def wrap(source: Sequence[int]) -> ImmutableSequenceView[int]:
    """Wrap a sequence of integers inside an immutable sequence view."""
    return ImmutableSequenceView[int](source)


def test_immutable_sequence_index() -> None:
    tester = wrap([1, 2, 3, 4, 5])
    assert tester.index(1) == 0
    with pytest.raises(ValueError):
        _ = tester.index(11)


def test_reverse_immutable_sequence() -> None:
    assert list(reversed(wrap([1, 2]))) == [2, 1]
