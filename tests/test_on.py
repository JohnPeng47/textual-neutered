from __future__ import annotations

from dataclasses import dataclass

import pytest

from textual import on
from textual._on import OnDecoratorError
from textual.app import App, ComposeResult
from textual.events import Enter, Leave
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, TabbedContent, TabPane


class MessageSender(Widget):
    @dataclass
    class Parent(Message):
        sender: MessageSender

        @property
        def control(self) -> MessageSender:
            return self.sender

    class Child(Parent):
        pass

    def post_parent(self) -> None:
        self.post_message(self.Parent(self))

    def post_child(self) -> None:
        self.post_message(self.Child(self))


class MixinMessageSender(Widget):
    class Parent(Message):
        pass

    class JustSomeRandomMixin:
        pass

    class Child(JustSomeRandomMixin, Parent):
        pass

    def post_parent(self) -> None:
        self.post_message(self.Parent())

    def post_child(self) -> None:
        self.post_message(self.Child())


async def test_fire_on_inherited_message_plus_mixins() -> None:
    """Handlers should fire when descendant messages are posted, without mixins messing things up."""

    posted: list[str] = []

    class InheritTestApp(App[None]):
        def compose(self) -> ComposeResult:
            yield MixinMessageSender()

        @on(MixinMessageSender.Parent)
        def catch_parent(self) -> None:
            posted.append("parent")

        @on(MixinMessageSender.Child)
        def catch_child(self) -> None:
            posted.append("child")

        def on_mount(self) -> None:
            self.query_one(MixinMessageSender).post_parent()
            self.query_one(MixinMessageSender).post_child()

    async with InheritTestApp().run_test():
        pass

    assert posted == ["parent", "child", "parent"]


async def test_on_with_enter_and_leave_events():
    class EnterLeaveApp(App):
        messages = []

        def compose(self) -> ComposeResult:
            yield Button("OK")

        @on(Enter, "Button")
        @on(Leave, "Button")
        def record(self, event: Enter | Leave) -> None:
            self.messages.append(event.__class__.__name__)

    app = EnterLeaveApp()
    async with app.run_test() as pilot:
        expected_messages = []

        await pilot.hover(Button)
        expected_messages.append("Enter")
        assert app.messages == expected_messages

        await pilot.hover(Button, offset=(0, 20))
        expected_messages.append("Leave")
        assert app.messages == expected_messages
