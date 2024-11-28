from __future__ import annotations

import pytest
from rich.panel import Panel
from rich.text import Text

from textual._wait import wait_for_idle
from textual.actions import SkipAction
from textual.app import App, ComposeResult, RenderableType
from textual.coordinate import Coordinate
from textual.geometry import Offset
from textual.message import Message
from textual.widgets import DataTable
from textual.widgets.data_table import (
    CellDoesNotExist,
    CellKey,
    ColumnDoesNotExist,
    ColumnKey,
    DuplicateKey,
    Row,
    RowDoesNotExist,
    RowKey,
)

ROWS = [["0/0", "0/1"], ["1/0", "1/1"], ["2/0", "2/1"]]


_DEFAULT_CELL_X_PADDING = 1


class DataTableApp(App):
    messages_to_record = {
        "CellHighlighted",
        "CellSelected",
        "RowHighlighted",
        "RowSelected",
        "ColumnHighlighted",
        "ColumnSelected",
        "HeaderSelected",
        "RowLabelSelected",
    }

    def __init__(self):
        super().__init__()
        self.messages = []

    def compose(self):
        table = DataTable()
        table.focus()
        yield table

    def record_data_table_event(self, message: Message) -> None:
        name = message.__class__.__name__
        if name in self.messages_to_record:
            self.messages.append(message)

    @property
    def message_names(self) -> list[str]:
        return [message.__class__.__name__ for message in self.messages]

    async def _on_message(self, message: Message) -> None:
        await super()._on_message(message)
        self.record_data_table_event(message)


async def test_move_cursor_respects_animate_parameter():
    """Regression test for https://github.com/Textualize/textual/issues/3840

    Make sure that the call to `_scroll_cursor_into_view` from `move_cursor` happens
    before the call from the watcher method from `cursor_coordinate`.
    The former should animate because we call it with `animate=True` whereas the later
    should not.
    """

    scrolls = []

    class _DataTable(DataTable):
        def _scroll_cursor_into_view(self, animate=False):
            nonlocal scrolls
            scrolls.append(animate)
            super()._scroll_cursor_into_view(animate)

    class LongDataTableApp(App):
        def compose(self):
            yield _DataTable()

        def on_mount(self):
            dt = self.query_one(_DataTable)
            dt.add_columns("one", "two")
            for _ in range(100):
                dt.add_row("one", "two")

        def key_s(self):
            table = self.query_one(_DataTable)
            table.move_cursor(row=99, animate=True)

    app = LongDataTableApp()
    async with app.run_test() as pilot:
        await pilot.press("s")

    assert scrolls == [True, False]


async def test_clicking_border_link_doesnt_crash():
    """Regression test for https://github.com/Textualize/textual/issues/4410"""

    class DataTableWithBorderLinkApp(App):
        CSS = """
        DataTable {
            border: solid red;
        }
        """
        link_clicked = False

        def compose(self) -> ComposeResult:
            yield DataTable()

        def on_mount(self) -> None:
            table = self.query_one(DataTable)
            table.border_title = "[@click=app.test_link]Border Link[/]"

        def action_test_link(self) -> None:
            self.link_clicked = True

    app = DataTableWithBorderLinkApp()
    async with app.run_test() as pilot:
        # Test clicking the link in the border doesn't crash with KeyError: 'row'
        await pilot.click(DataTable, offset=(5, 0))
        assert app.link_clicked is True
