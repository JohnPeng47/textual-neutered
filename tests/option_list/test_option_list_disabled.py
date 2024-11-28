"""Unit tests for testing an option list's disabled facility."""

from __future__ import annotations

import pytest

from textual.app import App, ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option, OptionDoesNotExist


class OptionListApp(App[None]):
    """Test option list application."""

    def __init__(self, disabled: bool) -> None:
        super().__init__()
        self.initial_disabled = disabled

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield OptionList(
            *[
                Option(str(n), id=str(n), disabled=self.initial_disabled)
                for n in range(100)
            ]
        )


async def test_enable_invalid_id() -> None:
    """Disabling an option via an ID that does not exist should throw an error."""
    async with OptionListApp(False).run_test() as pilot:
        with pytest.raises(OptionDoesNotExist):
            pilot.app.query_one(OptionList).enable_option("does-not-exist")


async def test_enable_invalid_index() -> None:
    """Disabling an option via an index that does not exist should throw an error."""
    async with OptionListApp(False).run_test() as pilot:
        with pytest.raises(OptionDoesNotExist):
            pilot.app.query_one(OptionList).enable_option_at_index(4242)
