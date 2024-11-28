from __future__ import annotations

import pytest

from textual.app import App, ComposeResult
from textual.widgets import Tree
from textual.widgets.tree import RemoveRootError


class VerseBody:
    pass


class VerseStar(VerseBody):
    pass


class VersePlanet(VerseBody):
    pass


class VerseMoon(VerseBody):
    pass


class VerseTree(Tree[VerseBody]):
    pass


class TreeClearApp(App[None]):
    """Tree clearing test app."""

    def compose(self) -> ComposeResult:
        yield VerseTree("White Sun", data=VerseStar())

    def on_mount(self) -> None:
        tree = self.query_one(VerseTree)
        node = tree.root.add("Londinium", VersePlanet())
        node.add_leaf("Balkerne", VerseMoon())
        node.add_leaf("Colchester", VerseMoon())
        node = tree.root.add("Sihnon", VersePlanet())
        node.add_leaf("Airen", VerseMoon())
        node.add_leaf("Xiaojie", VerseMoon())


async def test_tree_remove_children_of_root():
    """Test removing the children of the root."""
    async with TreeClearApp().run_test() as pilot:
        tree = pilot.app.query_one(VerseTree)
        assert len(tree.root.children) > 1
        tree.root.remove_children()
        assert len(tree.root.children) == 0


async def test_attempt_to_remove_root():
    """Attempting to remove the root should be an error."""
    async with TreeClearApp().run_test() as pilot:
        with pytest.raises(RemoveRootError):
            pilot.app.query_one(VerseTree).root.remove()
