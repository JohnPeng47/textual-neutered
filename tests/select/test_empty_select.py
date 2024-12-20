import pytest

from textual.app import App
from textual.widgets import Select
from textual.widgets.select import EmptySelectError


async def test_empty_select_raises_exception_if_allow_blank_is_false():
    class SelectApp(App[None]):
        def compose(self):
            yield Select([], allow_blank=False)

    app = SelectApp()
    with pytest.raises(EmptySelectError):
        async with app.run_test():
            pass


async def test_empty_set_options_raises_exception_if_allow_blank_is_false():
    class SelectApp(App[None]):
        def compose(self):
            yield Select([(str(n), n) for n in range(3)], allow_blank=False)

    app = SelectApp()
    async with app.run_test():
        select = app.query_one(Select)
        assert not select.is_blank()  # Sanity check.
        with pytest.raises(EmptySelectError):
            select.set_options([])
