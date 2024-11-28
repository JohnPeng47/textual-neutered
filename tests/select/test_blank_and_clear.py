import pytest

from textual.app import App
from textual.widgets import Select
from textual.widgets.select import InvalidSelectValueError

SELECT_OPTIONS = [(str(n), n) for n in range(3)]


async def test_clear_with_allow_blanks():
    class SelectApp(App[None]):
        def compose(self):
            yield Select(SELECT_OPTIONS, value=1)

    app = SelectApp()
    async with app.run_test():
        select = app.query_one(Select)
        assert select.value == 1  # Sanity check.
        select.clear()
        assert select.is_blank()


async def test_clear_fails_if_allow_blank_is_false():
    class SelectApp(App[None]):
        def compose(self):
            yield Select(SELECT_OPTIONS, allow_blank=False)

    app = SelectApp()
    async with app.run_test():
        select = app.query_one(Select)
        assert not select.is_blank()
        with pytest.raises(InvalidSelectValueError):
            select.clear()
