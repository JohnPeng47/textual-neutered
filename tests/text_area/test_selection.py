import pytest

from textual.app import App, ComposeResult
from textual.widgets import TextArea
from textual.widgets.text_area import Selection

TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
"""


class TextAreaApp(App):
    def compose(self) -> ComposeResult:
        text_area = TextArea()
        text_area.load_text(TEXT)
        yield text_area


async def test_cursor_screen_offset_and_terminal_cursor_position_scrolling():
    class TextAreaCursorScreenOffset(App):
        def compose(self) -> ComposeResult:
            yield TextArea.code_editor("AB\nAB\nAB\nAB\nAB\nAB\n")

    app = TextAreaCursorScreenOffset()
    async with app.run_test(size=(80, 2)) as pilot:
        text_area = app.query_one(TextArea)

        assert app.cursor_position == (5, 1)

        text_area.cursor_location = (5, 0)
        await pilot.pause()

        assert text_area.cursor_screen_offset == (5, 1)
        assert app.cursor_position == (5, 1)


async def test_mouse_selection_with_tab_characters():
    """Regression test for https://github.com/Textualize/textual/issues/5212"""

    class TextAreaTabsApp(App):
        def compose(self) -> ComposeResult:
            yield TextArea(soft_wrap=False, text="\t\t")

    app = TextAreaTabsApp()
    async with app.run_test() as pilot:
        text_area = pilot.app.query_one(TextArea)
        expected_selection = Selection((0, 0), (0, 0))
        assert text_area.selection == expected_selection

        await pilot.mouse_down(text_area, offset=(2, 1))
        await pilot.hover(text_area, offset=(3, 1))

        assert text_area.selection == expected_selection
