import pytest

from textual._arrange import TOP_Z, arrange
from textual.app import App
from textual.geometry import NULL_OFFSET, Region, Size, Spacing
from textual.layout import WidgetPlacement
from textual.widget import Widget


def test_arrange_dock_bottom():
    container = Widget(id="container")
    container._parent = App()
    child = Widget(id="child")
    header = Widget(id="header")
    header.styles.dock = "bottom"
    header.styles.height = "1"

    result = arrange(container, [child, header], Size(80, 24), Size(80, 24))
    assert result.placements == [
        WidgetPlacement(
            Region(0, 23, 80, 1),
            NULL_OFFSET,
            Spacing(),
            header,
            order=TOP_Z,
            fixed=True,
        ),
        WidgetPlacement(
            Region(0, 0, 80, 23), NULL_OFFSET, Spacing(), child, order=0, fixed=False
        ),
    ]
    assert result.widgets == {child, header}


def test_arrange_dock_badly():
    child = Widget(id="child")
    child.styles.dock = "nowhere"
    with pytest.raises(AssertionError):
        _ = arrange(Widget(), [child], Size(80, 24), Size(80, 24))
