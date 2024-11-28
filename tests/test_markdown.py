"""Unit tests for the Markdown widget."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pytest
from markdown_it.token import Token
from rich.style import Style
from rich.text import Span

import textual.widgets._markdown as MD
from textual import on
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Markdown
from textual.widgets.markdown import MarkdownBlock


class UnhandledToken(MarkdownBlock):
    def __init__(self, markdown: Markdown, token: Token) -> None:
        super().__init__(markdown)
        self._token = token

    def __repr___(self) -> str:
        return self._token.type


class FussyMarkdown(Markdown):
    def unhandled_token(self, token: Token) -> MarkdownBlock | None:
        return UnhandledToken(self, token)


class MarkdownApp(App[None]):
    def __init__(self, markdown: str) -> None:
        super().__init__()
        self._markdown = markdown

    def compose(self) -> ComposeResult:
        yield FussyMarkdown(self._markdown)


async def test_link_in_markdown_table_posts_message_when_clicked():
    """A link inside a markdown table should post a `Markdown.LinkClicked`
    message when clicked.

    Regression test for https://github.com/Textualize/textual/issues/4683
    """

    markdown_table = """\
| Textual Links                                    |
| ------------------------------------------------ |
| [GitHub](https://github.com/textualize/textual/) |
| [Documentation](https://textual.textualize.io/)  |\
"""

    class MarkdownTableApp(App):
        messages = []

        def compose(self) -> ComposeResult:
            yield Markdown(markdown_table, open_links=False)

        @on(Markdown.LinkClicked)
        def log_markdown_link_clicked(
            self,
            event: Markdown.LinkClicked,
        ) -> None:
            self.messages.append(event.__class__.__name__)

    app = MarkdownTableApp()
    async with app.run_test() as pilot:
        await pilot.click(Markdown, offset=(3, 3))
        assert app.messages == ["LinkClicked"]


async def test_markdown_quoting():
    # https://github.com/Textualize/textual/issues/3350
    links = []

    class MyApp(App):
        def compose(self) -> ComposeResult:
            self.md = Markdown(markdown="[tété](tété)", open_links=False)
            yield self.md

        def on_markdown_link_clicked(self, message: Markdown.LinkClicked):
            links.append(message.href)

    app = MyApp()
    async with app.run_test() as pilot:
        await pilot.click(Markdown, offset=(3, 0))
    assert links == ["tété"]
