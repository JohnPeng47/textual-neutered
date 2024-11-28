from __future__ import annotations

import asyncio

import pytest

from textual.app import App, ComposeResult
from textual.message import Message
from textual.message_pump import MessagePump
from textual.reactive import Reactive, TooManyComputesError, reactive, var
from textual.widget import Widget

OLD_VALUE = 5_000
NEW_VALUE = 1_000_000


async def test_mutate_reactive() -> None:
    """Test explicitly mutating reactives"""

    watched_names: list[list[str]] = []

    class TestWidget(Widget):
        names: reactive[list[str]] = reactive(list)

        def watch_names(self, names: list[str]) -> None:
            watched_names.append(names.copy())

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield TestWidget()

    app = TestApp()
    async with app.run_test():
        widget = app.query_one(TestWidget)
        # watch method called on startup
        assert watched_names == [[]]

        # Mutate the list
        widget.names.append("Paul")
        # No changes expected
        assert watched_names == [[]]
        # Explicitly mutate the reactive
        widget.mutate_reactive(TestWidget.names)
        # Watcher will be invoked
        assert watched_names == [[], ["Paul"]]
        # Make further modifications
        widget.names.append("Jessica")
        widget.names.remove("Paul")
        # No change expected
        assert watched_names == [[], ["Paul"]]
        # Explicit mutation
        widget.mutate_reactive(TestWidget.names)
        # Watcher should be invoked
        assert watched_names == [[], ["Paul"], ["Jessica"]]


async def test_mutate_reactive_data_bind() -> None:
    """https://github.com/Textualize/textual/issues/4825"""

    # Record mutations to TestWidget.messages
    widget_messages: list[list[str]] = []

    class TestWidget(Widget):
        messages: reactive[list[str]] = reactive(list, init=False)

        def watch_messages(self, names: list[str]) -> None:
            widget_messages.append(names.copy())

    class TestApp(App):
        messages: reactive[list[str]] = reactive(list, init=False)

        def compose(self) -> ComposeResult:
            yield TestWidget().data_bind(TestApp.messages)

    app = TestApp()
    async with app.run_test():
        test_widget = app.query_one(TestWidget)
        assert widget_messages == [[]]
        assert test_widget.messages == []

        # Should be the same instance
        assert app.messages is test_widget.messages

        # Mutate app
        app.messages.append("foo")
        # Mutations aren't detected
        assert widget_messages == [[]]
        assert app.messages == ["foo"]
        assert test_widget.messages == ["foo"]
        # Explicitly mutate app reactive
        app.mutate_reactive(TestApp.messages)
        # Mutating app, will also invoke watchers on any data binds
        assert widget_messages == [[], ["foo"]]
        assert app.messages == ["foo"]
        assert test_widget.messages == ["foo"]
