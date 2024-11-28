from contextlib import nullcontext as does_not_raise

import pytest

from textual.color import Color
from textual.css.stylesheet import CssSource, Stylesheet, StylesheetParseError
from textual.css.tokenizer import TokenError
from textual.dom import DOMNode
from textual.geometry import Spacing
from textual.widget import Widget


def _make_user_stylesheet(css: str) -> Stylesheet:
    stylesheet = Stylesheet()
    stylesheet.source["test.tcss"] = CssSource(css, is_defaults=False)
    stylesheet.parse()
    return stylesheet


@pytest.mark.parametrize(
    "css_property_name,expected_property_name_suggestion",
    [
        ["backgroundu", "background"],
        ["bckgroundu", "background"],
        ["ofset-x", "offset-x"],
        ["ofst_y", "offset-y"],
        ["colr", "color"],
        ["colour", "color"],
        ["wdth", "width"],
        ["wth", "width"],
        ["wh", None],
        ["xkcd", None],
    ],
)
def test_did_you_mean_for_property_names_in_nested_css(
    css_property_name: str, expected_property_name_suggestion: "str | None"
) -> None:
    """Test that we get nice errors with mistyped declaractions in nested CSS.

    When implementing pseudo-class support in nested TCSS
    (https://github.com/Textualize/textual/issues/4039), the first iterations didn't
    preserve this so we add these tests to make sure we don't take this feature away
    unintentionally.
    """
    stylesheet = Stylesheet()
    css = """
    Screen {
        * {
            border: blue;
            ${PROPERTY}: red;
        }
    }
    """.replace(
        "${PROPERTY}", css_property_name
    )

    stylesheet.add_source(css)
    with pytest.raises(StylesheetParseError) as err:
        stylesheet.parse()

    _, help_text = err.value.errors.rules[1].errors[0]
    displayed_css_property_name = css_property_name.replace("_", "-")
    expected_summary = f"Invalid CSS property {displayed_css_property_name!r}"
    if expected_property_name_suggestion:
        expected_summary += f". Did you mean '{expected_property_name_suggestion}'?"
    assert help_text.summary == expected_summary


@pytest.mark.parametrize(
    "css_property_name,css_property_value,expected_color_suggestion",
    [
        ["color", "blu", "blue"],
        ["background", "chartruse", "chartreuse"],
        ["tint", "ansi_whi", "ansi_white"],
        ["scrollbar-color", "transprnt", "transparent"],
        ["color", "xkcd", None],
    ],
)
def test_did_you_mean_for_color_names(
    css_property_name: str, css_property_value: str, expected_color_suggestion
):
    stylesheet = Stylesheet()
    css = """
    * {
      border: blue;
      ${PROPERTY}: ${VALUE};
    }
    """.replace(
        "${PROPERTY}", css_property_name
    ).replace(
        "${VALUE}", css_property_value
    )

    stylesheet.add_source(css)
    with pytest.raises(StylesheetParseError) as err:
        stylesheet.parse()

    _, help_text = err.value.errors.rules[0].errors[0]  # type: Any, HelpText
    displayed_css_property_name = css_property_name.replace("_", "-")
    expected_error_summary = f"Invalid value ({css_property_value!r}) for the [i]{displayed_css_property_name}[/] property"

    if expected_color_suggestion is not None:
        expected_error_summary += f". Did you mean '{expected_color_suggestion}'?"

    assert help_text.summary == expected_error_summary
