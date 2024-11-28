from operator import attrgetter

import pytest
from rich.text import Text

from textual import events
from textual._node_list import DuplicateIds
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.css.errors import StyleValueError
from textual.css.query import NoMatches
from textual.geometry import Offset, Size
from textual.message import Message
from textual.visual import RichVisual
from textual.widget import BadWidgetName, MountError, PseudoClasses, Widget
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    LoadingIndicator,
    Log,
    OptionList,
    RichLog,
    Switch,
    TextArea,
)


class GetByIdApp(App):
    def compose(self) -> ComposeResult:
        grandchild1 = Widget(id="grandchild1")
        child1 = Widget(grandchild1, id="child1")
        child2 = Widget(id="child2")

        yield Widget(
            child1,
            child2,
            id="parent",
        )

    @property
    def parent(self) -> Widget:
        return self.query_one("#parent")


@pytest.fixture
async def hierarchy_app():
    app = GetByIdApp()
    yield app


# Regression test for https://github.com/Textualize/textual/issues/1634


# Regression test for https://github.com/Textualize/textual/issues/2079


def test_lazy_loading() -> None:
    """Regression test for https://github.com/Textualize/textual/issues/5077

    Check that the lazy loading magic doesn't break attribute access.

    """

    with pytest.raises(ImportError):
        from textual.widgets import Foo  # nopycln: import

    from textual import widgets
    from textual.widgets import Label

    assert not hasattr(widgets, "foo")
    assert not hasattr(widgets, "bar")
    assert hasattr(widgets, "Label")


async def test_of_type() -> None:
    class MyApp(App):
        def compose(self) -> ComposeResult:
            for ordinal in range(5):
                yield Label(f"Item {ordinal}")

    app = MyApp()
    async with app.run_test():
        labels = list(app.query(Label))
        assert labels[0].first_of_type
        assert not labels[0].last_of_type
        assert labels[0].is_odd
        assert not labels[0].is_even

        assert not labels[1].first_of_type
        assert not labels[1].last_of_type
        assert not labels[1].is_odd
        assert labels[1].is_even

        assert not labels[2].first_of_type
        assert not labels[2].last_of_type
        assert labels[2].is_odd
        assert not labels[2].is_even

        assert not labels[3].first_of_type
        assert not labels[3].last_of_type
        assert not labels[3].is_odd
        assert labels[3].is_even

        assert not labels[4].first_of_type
        assert labels[4].last_of_type
        assert labels[4].is_odd
        assert not labels[4].is_even
