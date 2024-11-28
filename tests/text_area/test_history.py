from __future__ import annotations

import dataclasses

import pytest

from textual.app import App, ComposeResult
from textual.events import Paste
from textual.widgets import TextArea
from textual.widgets.text_area import EditHistory, Selection

MAX_CHECKPOINTS = 5
SIMPLE_TEXT = """\
ABCDE
FGHIJ
KLMNO
PQRST
UVWXY
Z
"""


@dataclasses.dataclass
class TimeMockableEditHistory(EditHistory):
    mock_time: float | None = dataclasses.field(default=None, init=False)

    def _get_time(self) -> float:
        """Return the mocked time if it is set, otherwise use default behaviour."""
        if self.mock_time is None:
            return super()._get_time()
        return self.mock_time


class TextAreaApp(App):
    def compose(self) -> ComposeResult:
        text_area = TextArea()
        # Update the history object to a version that supports mocking the time.
        text_area.history = TimeMockableEditHistory(
            max_checkpoints=MAX_CHECKPOINTS,
            checkpoint_timer=2.0,
            checkpoint_max_characters=100,
        )
        self.text_area = text_area
        yield text_area


@pytest.fixture
async def pilot():
    app = TextAreaApp()
    async with app.run_test() as pilot:
        yield pilot


@pytest.fixture
async def text_area(pilot):
    return pilot.app.text_area


async def test_redo_stack():
    app = TextAreaApp()
    async with app.run_test() as pilot:
        text_area = app.text_area
        assert len(text_area.history.redo_stack) == 0
        await pilot.press("enter")
        await pilot.press(*"123")
        assert len(text_area.history.undo_stack) == 2
        assert len(text_area.history.redo_stack) == 0
        text_area.undo()
        assert len(text_area.history.undo_stack) == 1
        assert len(text_area.history.redo_stack) == 1
        text_area.undo()
        assert len(text_area.history.undo_stack) == 0
        assert len(text_area.history.redo_stack) == 2
        text_area.redo()
        assert len(text_area.history.undo_stack) == 1
        assert len(text_area.history.redo_stack) == 1
        text_area.redo()
        assert len(text_area.history.undo_stack) == 2
        assert len(text_area.history.redo_stack) == 0


async def test_backward_selection_undo_redo():
    app = TextAreaApp()
    async with app.run_test() as pilot:
        text_area = app.text_area
        # Failed prior to https://github.com/Textualize/textual/pull/4352
        text_area.text = SIMPLE_TEXT
        text_area.selection = Selection((3, 2), (0, 0))

        await pilot.press("a")

        text_area.undo()
        await pilot.press("down", "down", "down", "down")

        assert text_area.text == SIMPLE_TEXT
