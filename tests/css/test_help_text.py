import pytest

from tests.utilities.render import render
from textual.css._help_text import (
    align_help_text,
    border_property_help_text,
    color_property_help_text,
    fractional_property_help_text,
    layout_property_help_text,
    offset_property_help_text,
    offset_single_axis_help_text,
    scalar_help_text,
    spacing_invalid_value_help_text,
    spacing_wrong_number_of_values_help_text,
    string_enum_help_text,
    style_flags_property_help_text,
)


@pytest.fixture(params=["css", "inline"])
def styling_context(request):
    return request.param


def test_offset_single_axis_help_text():
    rendered = render(offset_single_axis_help_text("offset-x"))
    assert "Invalid value for" in rendered
    assert "offset-x" in rendered


def test_style_flags_property_help_text(styling_context):
    rendered = render(
        style_flags_property_help_text("text-style", "notavalue b", styling_context)
    )
    assert "Invalid value" in rendered
    assert "notavalue" in rendered

    if styling_context == "css":
        assert "text-style" in rendered
    else:
        assert "text_style" in rendered
