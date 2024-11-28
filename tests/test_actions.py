from __future__ import annotations

from typing import Any

import pytest

from textual.actions import ActionError, parse


@pytest.mark.parametrize(
    ["action_string", "expected_arguments"],
    [
        ("f('')", ("",)),
        ('f("")', ("",)),
        ("f('''''')", ("",)),
        ('f("""""")', ("",)),
        ("f('(')", ("(",)),
        ("f(')')", (")",)),  # Regression test for #2088
        ("f('f()')", ("f()",)),
    ],
)
def test_parse_action_nested_special_character_arguments(
    action_string: str, expected_arguments: tuple[Any]
) -> None:
    """Test that special characters nested in strings are handled correctly.

    See also: https://github.com/Textualize/textual/issues/2088
    """
    _, _, args = parse(action_string)
    assert args == expected_arguments


@pytest.mark.parametrize(
    "action_string",
    [
        "foo(,,,,,)",
        "bar(1 2 3 4 5)",
        "baz.spam(Tru, Fals, in)",
        "ham(not)",
        "cheese((((()",
    ],
)
def test_parse_action_raises_error(action_string: str) -> None:
    with pytest.raises(ActionError):
        parse(action_string)
