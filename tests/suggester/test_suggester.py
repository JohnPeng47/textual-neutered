from __future__ import annotations

import pytest

from textual.dom import DOMNode
from textual.suggester import Suggester, SuggestionReady


class FillSuggester(Suggester):
    async def get_suggestion(self, value: str):
        if len(value) <= 10:
            return f"{value:x<10}"


class LogListNode(DOMNode):
    def __init__(self, log_list: list[tuple[str, str]]) -> None:
        self.log_list = log_list

    def post_message(self, message: SuggestionReady):
        # We hijack post_message so we can intercept messages without creating a full app.
        self.log_list.append((message.suggestion, message.value))


@pytest.mark.parametrize(
    "value",
    [
        "hello",
        "HELLO",
        "HeLlO",
        "Hello",
        "hELLO",
    ],
)
async def test_case_insensitive_suggestions(value):
    class MySuggester(Suggester):
        async def get_suggestion(self, value: str):
            assert "hello" == value

    suggester = MySuggester(use_cache=False, case_sensitive=False)
    await suggester._get_suggestion(DOMNode(), value)


async def test_case_insensitive_cache_hits():
    count = 0

    class MySuggester(Suggester):
        async def get_suggestion(self, value: str):
            nonlocal count
            count += 1
            return value + "abc"

    suggester = MySuggester(use_cache=True, case_sensitive=False)
    hellos = ["hello", "HELLO", "HeLlO", "Hello", "hELLO"]
    for hello in hellos:
        await suggester._get_suggestion(DOMNode(), hello)
    assert count == 1
