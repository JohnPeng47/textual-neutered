from __future__ import annotations

from pathlib import Path

import pytest
from rich.panel import Panel
from rich.text import Text

from tests.snapshot_tests.language_snippets import SNIPPETS
from textual import events, on
from textual.app import App, ComposeResult
from textual.binding import Binding, Keymap
from textual.command import SimpleCommand
from textual.containers import Center, Container, Grid, Middle, Vertical, VerticalScroll
from textual.pilot import Pilot
from textual.renderables.gradient import LinearGradient
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Log,
    OptionList,
    Placeholder,
    ProgressBar,
    RadioSet,
    RichLog,
    Select,
    SelectionList,
    Static,
    Switch,
    Tab,
    Tabs,
    TextArea,
    TabbedContent,
    TabPane,
)
from textual.widgets.text_area import BUILTIN_LANGUAGES, Selection, TextAreaTheme
from textual.theme import Theme

# These paths should be relative to THIS directory.
WIDGET_EXAMPLES_DIR = Path("../../docs/examples/widgets")
LAYOUT_EXAMPLES_DIR = Path("../../docs/examples/guide/layout")
STYLES_EXAMPLES_DIR = Path("../../docs/examples/styles")
EXAMPLES_DIR = Path("../../examples")
SNAPSHOT_APPS_DIR = Path("./snapshot_apps")


# --- Layout related stuff ---


# --- Widgets - rendering and basic interactions ---
# Each widget should have a canonical example that is display in the docs.
# When adding a new widget, ideally we should also create a snapshot test
# from these examples which test rendering and simple interactions with it.


# --- CSS properties ---
# We have a canonical example for each CSS property that is shown in their docs.
# If any of these change, something has likely broken, so snapshot each of them.

PATHS = [
    path.name
    for path in (Path(__file__).parent / STYLES_EXAMPLES_DIR).iterdir()
    if path.suffix == ".py"
]


# --- Other ---


# --- textual-dev library preview tests ---


# --- Example apps ---
# We skip the code browser because the length of the scrollbar in the tree depends on
# the number of files and folders we have locally and that typically differs from the
# pristine setting in which CI runs.


def test_app_resize_order(snap_compare):
    """Regression test for https://github.com/Textualize/textual/issues/5284
    You should see a placeholder with text "BAR", focused and scrolled down so it fills the screen.
    """

    class FocusPlaceholder(Placeholder, can_focus=True):
        pass

    class NarrowScreen(Screen):
        AUTO_FOCUS = "#bar"

        def compose(self) -> ComposeResult:
            yield FocusPlaceholder("FOO", id="foo")
            yield FocusPlaceholder("BAR", id="bar")

    class SCApp(App):
        CSS = """
        Placeholder:focus {
            border: heavy white;
        }
        #foo {
            height: 24;
        }
        #bar {
            height: 1fr;
        }

        .narrow #bar {
            height: 100%;
        }

        """

        def on_mount(self) -> None:
            self.push_screen(NarrowScreen())

        def on_resize(self) -> None:
            self.add_class("narrow")

    snap_compare(SCApp())


def test_add_remove_tabs(snap_compare):
    """Regression test for https://github.com/Textualize/textual/issues/5215
    You should see a TabbedContent with three panes, entitled 'tab-2', 'New tab' and 'New tab'
    """

    class ExampleApp(App):
        BINDINGS = [
            ("r", "remove_pane", "Remove first pane"),
            ("a", "add_pane", "Add pane"),
        ]

        def compose(self) -> ComposeResult:
            with TabbedContent(initial="tab-2"):
                with TabPane("tab-1"):
                    yield Label("tab-1")
                with TabPane("tab-2"):
                    yield Label("tab-2")
            yield Footer()

        def action_remove_pane(self) -> None:
            tabbed_content = self.query_one(TabbedContent)
            tabbed_content.remove_pane("tab-1")

        def action_add_pane(self) -> None:
            tabbed_content = self.query_one(TabbedContent)
            new_pane = TabPane("New tab", Label("new"))
            tabbed_content.add_pane(new_pane)

    snap_compare(ExampleApp(), press=["a", "r", "a"])
