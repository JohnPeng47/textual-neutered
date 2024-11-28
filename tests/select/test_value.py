import pytest

from textual.app import App
from textual.widgets import Select
from textual.widgets.select import InvalidSelectValueError

SELECT_OPTIONS = [(str(n), n) for n in range(3)]
MORE_OPTIONS = [(str(n), n) for n in range(5, 8)]


class SelectApp(App[None]):
    def __init__(self, initial_value=Select.BLANK):
        self.initial_value = initial_value
        super().__init__()

    def compose(self):
        yield Select[int](SELECT_OPTIONS, value=self.initial_value)


async def test_initial_value_is_picked_if_allow_blank_is_false():
    """The initial value should be picked by default if allow_blank=False."""

    class SelectApp(App[None]):
        def compose(self):
            yield Select[int](SELECT_OPTIONS, allow_blank=False)

    app = SelectApp()
    async with app.run_test():
        assert app.query_one(Select).value == 0


async def test_initial_value_is_picked_if_allow_blank_is_false():
    """The initial value should be respected even if allow_blank=False."""

    class SelectApp(App[None]):
        def compose(self):
            yield Select[int](SELECT_OPTIONS, value=2, allow_blank=False)

    app = SelectApp()
    async with app.run_test():
        assert app.query_one(Select).value == 2


async def test_set_value_to_blank_with_allow_blank_false():
    """Setting the value to BLANK with allow_blank=False should raise an error."""

    class SelectApp(App[None]):
        def compose(self):
            yield Select[int](SELECT_OPTIONS, allow_blank=False)

    app = SelectApp()
    async with app.run_test():
        with pytest.raises(InvalidSelectValueError):
            app.query_one(Select).value = Select.BLANK


async def test_set_options_resets_value_to_blank():
    """Resetting the options should reset the value to BLANK."""

    class SelectApp(App[None]):
        def compose(self):
            yield Select[int](SELECT_OPTIONS, value=2)

    app = SelectApp()
    async with app.run_test():
        select = app.query_one(Select)
        assert select.value == 2
        select.set_options(MORE_OPTIONS)
        assert select.is_blank()


async def test_set_options_resets_value_if_allow_blank_is_false():
    """Resetting the options should reset the value if allow_blank=False."""

    class SelectApp(App[None]):
        def compose(self):
            yield Select[int](SELECT_OPTIONS, allow_blank=False)

    app = SelectApp()
    async with app.run_test():
        select = app.query_one(Select)
        assert select.value == 0
        select.set_options(MORE_OPTIONS)
        assert select.value > 2
