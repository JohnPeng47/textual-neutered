import pytest

from textual.widgets import Tree
from textual.widgets.tree import AddNodeError


def test_tree_node_add_after_node():
    tree = Tree[None]("root")
    node = tree.root.add("node")
    after_node = tree.root.add("after node", after=node)
    first = tree.root.add("first", after=-3)
    after_first = tree.root.add("after first", after=first)
    tree.root.add("before node", after=after_first)
    before_last = tree.root.add("before last", after=after_node)
    tree.root.add("last", after=before_last)

    assert str(tree.root.children[0].label) == "first"
    assert str(tree.root.children[1].label) == "after first"
    assert str(tree.root.children[2].label) == "before node"
    assert str(tree.root.children[3].label) == "node"
    assert str(tree.root.children[4].label) == "after node"
    assert str(tree.root.children[5].label) == "before last"
    assert str(tree.root.children[6].label) == "last"


def test_tree_node_add_leaf_before_or_after():
    tree = Tree[None]("root")
    leaf = tree.root.add_leaf("leaf")
    tree.root.add_leaf("before leaf", before=leaf)
    tree.root.add_leaf("after leaf", after=leaf)
    tree.root.add_leaf("first", before=0)
    tree.root.add_leaf("last", after=-1)

    assert str(tree.root.children[0].label) == "first"
    assert str(tree.root.children[1].label) == "before leaf"
    assert str(tree.root.children[2].label) == "leaf"
    assert str(tree.root.children[3].label) == "after leaf"
    assert str(tree.root.children[4].label) == "last"
