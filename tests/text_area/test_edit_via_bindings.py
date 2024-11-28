"""Tests some edits using the keyboard.

All tests in this module should press keys on the keyboard which edit the document,
and check that the document content is updated as expected, as well as the cursor
location.

Note that more extensive testing for editing is done at the Document level.
"""

import pytest

from textual.app import App, ComposeResult
from textual.events import Paste
from textual.widgets import TextArea
from textual.widgets.text_area import Selection

TEXT = """I must not fear.
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
Z"""


class TextAreaApp(App):
    def compose(self) -> ComposeResult:
        text_area = TextArea.code_editor()
        text_area.load_text(TEXT)
        yield text_area


@pytest.mark.parametrize(
    "selection",
    [
        Selection(start=(1, 0), end=(3, 0)),
        Selection(start=(3, 0), end=(1, 0)),
    ],
)
async def test_paste(selection):
    app = TextAreaApp()
    async with app.run_test() as pilot:
        text_area = app.query_one(TextArea)
        text_area.text = SIMPLE_TEXT
        text_area.selection = selection

        app.post_message(Paste("a"))
        await pilot.pause()

        expected_text = """\
ABCDE
aPQRST
UVWXY
Z"""
        assert text_area.text == expected_text
        assert text_area.selection == Selection.cursor((1, 1))


async def test_paste_read_only_does_nothing():
    app = TextAreaApp()
    async with app.run_test() as pilot:
        text_area = app.query_one(TextArea)
        text_area.read_only = True

        app.post_message(Paste("hello"))
        await pilot.pause()

        assert text_area.text == TEXT  # No change
