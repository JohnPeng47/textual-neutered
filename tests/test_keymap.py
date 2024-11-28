from __future__ import annotations

from typing import Any

from textual.app import App, ComposeResult
from textual.binding import Binding, Keymap
from textual.dom import DOMNode
from textual.widget import Widget
from textual.widgets import Label


class Counter(App[None]):
    BINDINGS = [
        Binding(key="i,up", action="increment", id="app.increment"),
        Binding(key="d,down", action="decrement", id="app.decrement"),
    ]

    def __init__(self, keymap: Keymap, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.count = 0
        self.clashed_bindings: set[Binding] | None = None
        self.clashed_node: DOMNode | None = None
        self.keymap = keymap

    def compose(self) -> ComposeResult:
        yield Label("foo")

    def on_mount(self) -> None:
        self.set_keymap(self.keymap)

    def action_increment(self) -> None:
        self.count += 1

    def action_decrement(self) -> None:
        self.count -= 1

    def handle_bindings_clash(
        self, clashed_bindings: set[Binding], node: DOMNode
    ) -> None:
        self.clashed_bindings = clashed_bindings
        self.clashed_node = node


async def test_keymap_inherited_bindings_same_id():
    """When a child widget inherits from a parent widget, if they have
    a binding with the same ID, then both parent and child bindings will
    be overridden by the keymap (assuming the keymap has a mapping with the
    same ID)."""

    parent_counter = 0
    child_counter = 0

    class Parent(Widget, can_focus=True):
        BINDINGS = [
            Binding(key="x", action="increment", id="increment"),
        ]

        def action_increment(self) -> None:
            nonlocal parent_counter
            parent_counter += 1

    class Child(Parent):
        BINDINGS = [
            Binding(key="x", action="increment", id="increment"),
        ]

        def action_increment(self) -> None:
            nonlocal child_counter
            child_counter += 1

    class MyApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Parent()
            yield Child()

        def on_mount(self) -> None:
            self.set_keymap({"increment": "i"})

    app = MyApp()
    async with app.run_test() as pilot:
        # Default binding is unbound due to keymap.
        await pilot.press("x")
        assert parent_counter == 0
        assert child_counter == 0

        # New binding is active, parent is focused - action called.
        await pilot.press("i")
        assert parent_counter == 1
        assert child_counter == 0

        # Tab to focus the child.
        await pilot.press("tab")

        # Default binding results in no change.
        await pilot.press("x")
        assert parent_counter == 1
        assert child_counter == 0

        # New binding is active, child is focused - action called.
        await pilot.press("i")
        assert parent_counter == 1
        assert child_counter == 1


async def test_keymap_child_with_different_id_overridden():
    """Ensures that overriding a parent binding doesn't influence a child
    binding with a different ID."""

    parent_counter = 0
    child_counter = 0

    class Parent(Widget, can_focus=True):
        BINDINGS = [
            Binding(key="x", action="increment", id="parent.increment"),
        ]

        def action_increment(self) -> None:
            nonlocal parent_counter
            parent_counter += 1

    class Child(Parent):
        BINDINGS = [
            Binding(key="x", action="increment", id="child.increment"),
        ]

        def action_increment(self) -> None:
            nonlocal child_counter
            child_counter += 1

    class MyApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Parent()
            yield Child()

        def on_mount(self) -> None:
            self.set_keymap({"parent.increment": "i"})

    app = MyApp()
    async with app.run_test() as pilot:
        # Default binding is unbound due to keymap.
        await pilot.press("x")
        assert parent_counter == 0
        assert child_counter == 0

        # New binding is active, parent is focused - action called.
        await pilot.press("i")
        assert parent_counter == 1
        assert child_counter == 0

        # Tab to focus the child.
        await pilot.press("tab")

        # Default binding is still active on the child.
        await pilot.press("x")
        assert parent_counter == 1
        assert child_counter == 1

        # The binding from the keymap only affects the parent, so
        # pressing it with the child focused does nothing.
        await pilot.press("i")
        assert parent_counter == 1
        assert child_counter == 1
