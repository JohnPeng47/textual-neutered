import pytest

from textual.css.errors import StyleValueError
from textual.dom import BadIdentifier, DOMNode


@pytest.fixture
def search():
    """
        a
       / \
      b   c
     /   / \
    d   e   f
    """
    a = DOMNode(id="a")
    b = DOMNode(id="b")
    c = DOMNode(id="c")
    d = DOMNode(id="d")
    e = DOMNode(id="e")
    f = DOMNode(id="f")

    a._add_child(b)
    a._add_child(c)
    b._add_child(d)
    c._add_child(e)
    c._add_child(f)

    yield a


def test_walk_children_with_self_breadth(search):
    children = [
        node.id for node in search.walk_children(with_self=True, method="breadth")
    ]
    print(children)
    assert children == ["a", "b", "c", "d", "e", "f"]

    children = [
        node.id
        for node in search.walk_children(with_self=True, method="breadth", reverse=True)
    ]

    assert children == ["f", "e", "d", "c", "b", "a"]


@pytest.mark.parametrize(
    "identifier",
    [
        " bad",
        "  terrible  ",
        "worse!  ",
        "&ampersand",
        "amper&sand",
        "ampersand&",
        "2_leading_digits",
        "água",  # water
        "cão",  # dog
        "@'/.23",
    ],
)
def test_id_validation(identifier: str):
    """Regression tests for https://github.com/Textualize/textual/issues/3954."""
    with pytest.raises(BadIdentifier):
        DOMNode(id=identifier)
