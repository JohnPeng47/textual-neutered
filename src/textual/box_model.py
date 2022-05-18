from __future__ import annotations

from typing import Callable, NamedTuple

from .geometry import Size, Spacing
from .css.styles import StylesBase


class BoxModel(NamedTuple):
    """The result of `get_box_model`."""

    size: Size  # Content + padding + border
    margin: Spacing  # Additional margin


def get_box_model(
    styles: StylesBase,
    container: Size,
    viewport: Size,
    get_content_width: Callable[[Size, Size], int],
    get_content_height: Callable[[Size, Size, int], int],
) -> BoxModel:
    """Resolve the box model for this Styles.

    Args:
        styles (StylesBase): Styles object.
        container (Size): The size of the widget container.
        viewport (Size): The viewport size.
        get_auto_width (Callable): A callable which accepts container size and parent size and returns a width.
        get_auto_height (Callable): A callable which accepts container size and parent size and returns a height.

    Returns:
        BoxModel: A tuple with the size of the content area and margin.
    """

    has_rule = styles.has_rule
    width, height = container
    is_content_box = styles.box_sizing == "content-box"
    is_border_box = styles.box_sizing == "border-box"
    gutter = styles.padding + styles.border.spacing
    margin = styles.margin

    is_auto_width = styles.width and styles.width.is_auto
    is_auto_height = styles.height and styles.height.is_auto

    if styles.width is None:
        width = container.width - margin.width
    elif is_auto_width:
        # When width is auto, we want enough space to always fit the content
        width = get_content_width(
            (container - gutter.totals if is_border_box else container)
            - styles.margin.totals,
            viewport,
        )
        # width = min(container.width, width)

    else:
        width = styles.width.resolve_dimension(container, viewport)

    if styles.min_width is not None:
        min_width = styles.min_width.resolve_dimension(container, viewport)
        width = max(width, min_width)

    if styles.max_width is not None:
        max_width = styles.max_width.resolve_dimension(container, viewport)
        width = min(width, max_width)

    if styles.height is None:
        height = container.height - margin.height
    elif styles.height.is_auto:
        height = get_content_height(
            container - gutter.totals if is_border_box else container, viewport, width
        )
        if is_border_box:
            height += gutter.height
    else:
        height = styles.height.resolve_dimension(container, viewport)

    if styles.min_height is not None:
        min_height = styles.min_height.resolve_dimension(container, viewport)
        height = max(height, min_height)

    if styles.max_height is not None:
        max_height = styles.max_height.resolve_dimension(container, viewport)
        height = min(height, max_height)

    if is_border_box and is_auto_width:
        width += gutter.width

    if is_content_box:
        width += gutter.width
        height += gutter.height

    model = BoxModel(Size(width, height), margin)
    return model
