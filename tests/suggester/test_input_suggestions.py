import string

import pytest

from textual.app import App, ComposeResult
from textual.suggester import SuggestFromList
from textual.widgets import Input


class SuggestionsApp(App[ComposeResult]):
    def __init__(self, suggestions):
        self.suggestions = suggestions
        self.input = Input(suggester=SuggestFromList(self.suggestions))
        super().__init__()

    def compose(self) -> ComposeResult:
        yield self.input


@pytest.mark.parametrize(
    ("suggestion", "truncate_at"),
    [
        (".......", 3),
        ("hey there", 3),
        ("Olá, tudo bem?", 3),
        ("áàóãõñç", 2),
        (string.punctuation, 3),
        (string.punctuation[::-1], 5),
        (string.punctuation[::3], 5),
    ],
)
async def test_suggestion_with_special_characters(suggestion: str, truncate_at: int):
    app = SuggestionsApp([suggestion])
    async with app.run_test() as pilot:
        await pilot.press(*suggestion[:truncate_at])
        assert app.input._suggestion == suggestion


async def test_suggestion_priority():
    app = SuggestionsApp(["dog", "dad"])
    async with app.run_test() as pilot:
        await pilot.press("d")
        assert app.input._suggestion == "dog"
        await pilot.press("a")
        assert app.input._suggestion == "dad"
