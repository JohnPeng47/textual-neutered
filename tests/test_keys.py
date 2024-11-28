import pytest

from textual.app import App
from textual.binding import Binding
from textual.keys import _character_to_key, format_key, key_to_character


def test_get_key_display():
    app = App()

    assert app.get_key_display(Binding("p", "", "")) == "p"
    assert app.get_key_display(Binding("ctrl+p", "", "")) == "^p"
    assert app.get_key_display(Binding("right_square_bracket", "", "")) == "]"
    assert app.get_key_display(Binding("ctrl+right_square_bracket", "", "")) == "^]"
    assert (
        app.get_key_display(Binding("shift+ctrl+right_square_bracket", "", ""))
        == "shift+^]"
    )
    assert app.get_key_display(Binding("delete", "", "")) == "del"


def test_key_to_character():
    assert key_to_character("f") == "f"
    assert key_to_character("F") == "F"
    assert key_to_character("space") == " "
    assert key_to_character("ctrl+space") is None
    assert key_to_character("question_mark") == "?"
    assert key_to_character("foo") is None
