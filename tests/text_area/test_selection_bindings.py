import pytest

from textual.app import App, ComposeResult
from textual.geometry import Offset
from textual.widgets import TextArea
from textual.widgets.text_area import Selection

TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
"""


class TextAreaApp(App):
    def __init__(self, read_only: bool = False):
        super().__init__()
        self.read_only = read_only

    def compose(self) -> ComposeResult:
        yield TextArea(TEXT, show_line_numbers=True, read_only=self.read_only)


@pytest.fixture(params=[True, False])
async def app(request):
    """Each test that receives an `app` will execute twice.
    Once with read_only=True, and once with read_only=False.
    """
    return TextAreaApp(read_only=request.param)


async def test_select_line_binding(app: TextAreaApp):
    async with app.run_test() as pilot:
        text_area = app.query_one(TextArea)
        text_area.move_cursor((2, 2))

        await pilot.press("f6")

        assert text_area.selection == Selection((2, 0), (2, 56))


async def test_select_all_binding(app: TextAreaApp):
    async with app.run_test() as pilot:
        text_area = app.query_one(TextArea)

        await pilot.press("f7")

        assert text_area.selection == Selection((0, 0), (4, 0))
