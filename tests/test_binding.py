from string import ascii_lowercase

import pytest

from textual.app import App
from textual.binding import (
    Binding,
    BindingError,
    BindingsMap,
    InvalidBinding,
    NoBinding,
)

BINDING1 = Binding("a,b", action="action1", description="description1")
BINDING2 = Binding("c", action="action2", description="description2")
BINDING3 = Binding(" d   , e ", action="action3", description="description3")


@pytest.fixture
def bindings():
    yield BindingsMap([BINDING1, BINDING2])


@pytest.fixture
def more_bindings():
    yield BindingsMap([BINDING1, BINDING2, BINDING3])


def test_shown():
    bindings = BindingsMap(
        [
            Binding(
                key,
                action=f"action_{key}",
                description=f"Emits {key}",
                show=bool(ord(key) % 2),
            )
            for key in ascii_lowercase
        ]
    )
    assert len(bindings.shown_keys) == (len(ascii_lowercase) / 2)


def test_invalid_binding():
    with pytest.raises(InvalidBinding):

        class BrokenApp(App):
            BINDINGS = [(",,,", "foo", "Broken")]

    with pytest.raises(InvalidBinding):

        class BrokenApp(App):
            BINDINGS = [(", ,", "foo", "Broken")]
