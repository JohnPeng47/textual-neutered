from __future__ import annotations

import pytest

from textual.css.tokenize import tokenize
from textual.css.tokenizer import Token, TokenError

VALID_VARIABLE_NAMES = [
    "warning-text",
    "warning_text",
    "warningtext1",
    "1warningtext",
    "WarningText1",
    "warningtext_",
    "warningtext-",
    "_warningtext",
    "-warningtext",
]


@pytest.mark.parametrize(
    ["pseudo_class", "expected"],
    [
        ("blue", "blur"),
        ("br", "blur"),
        ("canfocus", "can-focus"),
        ("can_focus", "can-focus"),
        ("can-foc", "can-focus"),
        ("drk", "dark"),
        ("ark", "dark"),
        ("disssabled", "disabled"),
        ("enalbed", "enabled"),
        ("focoswithin", "focus-within"),
        ("focus_whitin", "focus-within"),
        ("fcus", "focus"),
        ("huver", "hover"),
        ("LIght", "light"),
    ],
)
def test_did_you_mean_pseudo_classes(pseudo_class: str, expected: str) -> None:
    """Make sure we get the correct suggestion for pseudo-classes with typos."""

    css = f"""
    Button:{pseudo_class} {{
        background: red;
    }}
    """

    with pytest.raises(TokenError) as err:
        list(tokenize(css, ("", "")))

    assert f"unknown pseudo-class {pseudo_class!r}" in str(err.value)
    assert f"did you mean {expected!r}" in str(err.value)


@pytest.mark.parametrize(
    ["pseudo_class", "expected"],
    [
        ("blue", "blur"),
        ("br", "blur"),
        ("canfocus", "can-focus"),
        ("can_focus", "can-focus"),
        ("can-foc", "can-focus"),
        ("drk", "dark"),
        ("ark", "dark"),
        ("disssabled", "disabled"),
        ("enalbed", "enabled"),
        ("focoswithin", "focus-within"),
        ("focus_whitin", "focus-within"),
        ("fcus", "focus"),
        ("huver", "hover"),
        ("LIght", "light"),
    ],
)
def test_did_you_mean_pseudo_classes_in_nested_css(
    pseudo_class: str, expected: str
) -> None:
    """Test that we get nice errors for pseudo-classes with typos in nested TCSS.

    When implementing pseudo-class support in nested TCSS
    (https://github.com/Textualize/textual/issues/4039), the first iterations didn't
    preserve this so we add these tests to make sure we don't take this feature away
    unintentionally.
    """

    css = f"""
    Screen {{
        Button:{pseudo_class} {{
            background: red;
        }}
    }}
    """

    with pytest.raises(TokenError) as err:
        list(tokenize(css, ("", "")))

    assert f"unknown pseudo-class {pseudo_class!r}" in str(err.value)
    assert f"did you mean {expected!r}" in str(err.value)
