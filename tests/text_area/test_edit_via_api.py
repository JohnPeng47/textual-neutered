"""Tests editing the document using the API (replace etc.)

The tests in this module directly call the edit APIs on the TextArea rather
than going via bindings.

Note that more extensive testing for editing is done at the Document level.
"""

import pytest

from textual.app import App, ComposeResult
from textual.widgets import TextArea
from textual.widgets.text_area import EditResult, Selection

TEXT = """\
I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
"""

SIMPLE_TEXT = """\
ABCDE
FGHIJ
KLMNO
PQRST
UVWXY
Z
"""


class TextAreaApp(App):
    def compose(self) -> ComposeResult:
        text_area = TextArea()
        text_area.load_text(TEXT)
        yield text_area


async def test_text_setter():
    app = TextAreaApp()
    async with app.run_test():
        text_area = app.query_one(TextArea)
        new_text = "hello\nworld\n"
        text_area.text = new_text
        assert text_area.text == new_text


async def test_edits_on_read_only_mode():
    """API edits should still be permitted on read-only mode."""
    app = TextAreaApp()
    async with app.run_test():
        text_area = app.query_one(TextArea)
        text_area.text = "0123456789"
        text_area.read_only = True

        text_area.replace("X", (0, 1), (0, 5))
        assert text_area.text == "0X56789"

        text_area.insert("X")
        assert text_area.text == "X0X56789"

        text_area.delete((0, 0), (0, 2))
        assert text_area.text == "X56789"
