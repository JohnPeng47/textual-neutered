from __future__ import annotations

import pytest

from textual.app import App, ComposeResult
from textual.color import Color
from textual.containers import Vertical
from textual.css.parse import parse
from textual.css.tokenizer import EOFError, TokenError
from textual.widgets import Button, Label


class NestedApp(App):
    CSS = """
    Screen {
        & > #foo {
            background: red;
            #egg {
                background: green;
            }
            .paul {
                background: blue;
            }
            &.jessica {
                color: magenta;
            }
        }
    }    
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="foo", classes="jessica"):
            yield Label("Hello", id="egg")
            yield Label("World", classes="paul")


class ListOfNestedSelectorsApp(App[None]):
    CSS = """
    Label {
        &.foo, &.bar {
            background: red;
        }
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("one", classes="foo")
        yield Label("two", classes="bar")
        yield Label("three", classes="heh")


class DeclarationAfterNestedApp(App[None]):
    CSS = """
    Screen {
        background: green;
        Label {
            background: red;
        }        
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("one")


@pytest.mark.parametrize(
    ("css", "exception"),
    [
        ("Selector {", EOFError),
        ("Selector{ Foo {", EOFError),
        ("Selector{ Foo {}", EOFError),
        ("> {}", TokenError),
        ("&", TokenError),
        ("&&", TokenError),
        ("&.foo", TokenError),
        ("& .foo", TokenError),
        ("{", TokenError),
        ("*{", EOFError),
    ],
)
def test_parse_errors(css: str, exception: type[Exception]) -> None:
    """Check some CSS which should fail."""
    with pytest.raises(exception):
        list(parse("", css, ("foo", "")))


class PseudoClassesInNestedApp(App[None]):
    CSS = """
    Vertical {
        Button:light, Button:dark {
            background: red;
        }

        min-height: 3;  # inconsequential rule to add entropy.

        #two, *:focus {
            background: green !important;
        }

        height: auto;  # inconsequential rule to add entropy.

        Label {
            background: yellow;

            &:light, &:dark {
                background: red;
            }

            &:hover {
                background: green !important;
            }
        }
    }
    """

    AUTO_FOCUS = "Button"

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button(id="one", classes="first_half")
            yield Button(id="two", classes="first_half")
        with Vertical():
            yield Label("Hello, world!", id="three", classes="first_half")
            yield Label("Hello, world!", id="four", classes="first_half")
        with Vertical():
            yield Button(id="five", classes="second_half")
            yield Button(id="six", classes="second_half")
            yield Label("Hello, world!", id="seven", classes="second_half")
            yield Label("Hello, world!", id="eight", classes="second_half")


async def test_pseudo_classes_work_in_nested_css() -> None:
    """Makes sure pseudo-classes are correctly understood in nested TCSS.

    Regression test for https://github.com/Textualize/textual/issues/4039.
    """

    app = PseudoClassesInNestedApp()
    green = Color.parse("green")
    red = Color.parse("red")
    async with app.run_test() as pilot:
        assert app.query_one("#one").styles.background == green
        assert app.query_one("#two").styles.background == green
        assert app.query_one("#five").styles.background == red
        assert app.query_one("#six").styles.background == red

        assert app.query_one("#three").styles.background == red
        assert app.query_one("#four").styles.background == red
        assert app.query_one("#seven").styles.background == red
        assert app.query_one("#eight").styles.background == red

        await pilot.hover("#eight")

        assert app.query_one("#three").styles.background == red
        assert app.query_one("#four").styles.background == red
        assert app.query_one("#seven").styles.background == red
        assert app.query_one("#eight").styles.background == green
