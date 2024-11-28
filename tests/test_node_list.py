import pytest

from textual._node_list import NodeList
from textual.widget import Widget


def test_clear():
    """Can we clear the list?"""
    nodes = NodeList()
    assert len(nodes) == 0
    widgets = [Widget() for _ in range(1000)]
    for widget in widgets:
        nodes._append(widget)
    assert len(nodes) == 1000
    for widget in widgets:
        assert widget in nodes
    nodes._clear()
    assert len(nodes) == 0
    for widget in widgets:
        assert widget not in nodes


def test_listy():
    nodes = NodeList()
    widget1 = Widget()
    widget2 = Widget()
    nodes._append(widget1)
    nodes._append(widget2)
    assert list(nodes) == [widget1, widget2]
    assert list(reversed(nodes)) == [widget2, widget1]
    assert nodes[0] == widget1
    assert nodes[1] == widget2
    assert nodes[0:2] == [widget1, widget2]
