from __future__ import annotations

from pathlib import Path

from rich.text import Text

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree


class DirectoryTreeApp(App[None]):
    """DirectoryTree test app."""

    def __init__(self, path):
        super().__init__()
        self._tmp_path = path
        self.messages = []

    def compose(self) -> ComposeResult:
        yield DirectoryTree(self._tmp_path)

    @on(DirectoryTree.FileSelected)
    @on(DirectoryTree.DirectorySelected)
    def record(
        self, event: DirectoryTree.FileSelected | DirectoryTree.DirectorySelected
    ) -> None:
        self.messages.append(event.__class__.__name__)


async def test_directory_tree_reload_other_node(tmp_path: Path) -> None:
    """Reloading a node of a directory tree should not reload content of other directory."""

    RELOADED_DIRECTORY = "parentdir"
    NOT_RELOADED_DIRECTORY = "otherdir"
    FILE1_NAME = "log.txt"
    NOT_RELOADED_FILE3_NAME = "demo.txt"
    NOT_RELOADED_FILE4_NAME = "unseen.txt"

    # Creating two nodes, each having one file as child
    reloaded_dir = tmp_path / RELOADED_DIRECTORY
    reloaded_dir.mkdir()
    file1 = reloaded_dir / FILE1_NAME
    file1.touch()
    non_reloaded_dir = tmp_path / NOT_RELOADED_DIRECTORY
    non_reloaded_dir.mkdir()
    file3 = non_reloaded_dir / NOT_RELOADED_FILE3_NAME
    file3.touch()

    async with DirectoryTreeApp(tmp_path).run_test() as pilot:
        tree = pilot.app.query_one(DirectoryTree)
        await pilot.pause()

        # Sanity check - the root has the two nodes as its children (in alphabetical order)
        assert len(tree.root.children) == 2
        unaffected_node = tree.root.children[0]
        node = tree.root.children[1]
        assert unaffected_node.label == Text(NOT_RELOADED_DIRECTORY)
        assert node.label == Text(RELOADED_DIRECTORY)
        unaffected_node.expand()
        node.expand()
        await pilot.pause()
        assert len(unaffected_node.children) == 1
        assert unaffected_node.children[0].label == Text(NOT_RELOADED_FILE3_NAME)

        # Creating new file under the node that won't be reloaded
        file4 = non_reloaded_dir / NOT_RELOADED_FILE4_NAME
        file4.touch()

        tree.reload_node(node)
        node.collapse()
        node.expand()
        unaffected_node.collapse()
        unaffected_node.expand()
        await pilot.pause()

        # After reloading one node, the new file under the other one does not show up
        assert len(unaffected_node.children) == 1
        assert unaffected_node.children[0].label == Text(NOT_RELOADED_FILE3_NAME)


async def test_directory_tree_reloading_preserves_state(tmp_path: Path) -> None:
    """Regression test for https://github.com/Textualize/textual/issues/4122.

    Ensures `clear_node` does clear the node specified.
    """
    ROOT = "root"
    structure = [
        ROOT,
        "root/file1.txt",
        "root/file2.txt",
    ]

    for path in structure:
        if path.endswith(".txt"):
            (tmp_path / path).touch()
        else:
            (tmp_path / path).mkdir()

    app = DirectoryTreeApp(tmp_path / ROOT)
    async with app.run_test() as pilot:
        directory_tree = app.query_one(DirectoryTree)
        directory_tree.clear_node(directory_tree.root)
        await pilot.pause()
        assert not directory_tree.root.children
