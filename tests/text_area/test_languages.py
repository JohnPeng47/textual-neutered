import pytest

from textual.app import App, ComposeResult
from textual.widgets import TextArea
from textual.widgets.text_area import (
    Document,
    LanguageDoesNotExist,
    SyntaxAwareDocument,
)


class TextAreaApp(App):
    def compose(self) -> ComposeResult:
        yield TextArea("print('hello')", language="python")


@pytest.mark.syntax
async def test_register_language_existing_language():
    app = TextAreaApp()
    async with app.run_test():
        text_area = app.query_one(TextArea)

        # Before registering the language, we have highlights as expected.
        assert len(text_area._highlights) > 0

        # Overwriting the highlight query for Python...
        text_area.register_language("python", "")

        # We've overridden the highlight query with a blank one, so there are no highlights.
        assert text_area._highlights == {}


@pytest.mark.syntax
async def test_language_binary_missing(monkeypatch: pytest.MonkeyPatch):
    # mock a failed installation of tree-sitter-language binaries by
    # raising an OSError from get_language
    def raise_oserror(_):
        raise OSError(
            "/path/to/tree_sitter_languages/languages.so: "
            "cannot open shared object file: No such file or directory"
        )

    monkeypatch.setattr(
        "textual.document._syntax_aware_document.get_language", raise_oserror
    )

    app = TextAreaApp()
    async with app.run_test():
        text_area = app.query_one(TextArea)  # does not crash
        assert text_area.language == "python"
        # resulting document is not a SyntaxAwareDocument and does not
        # support highlights
        assert isinstance(text_area.document, Document)
        assert not isinstance(text_area.document, SyntaxAwareDocument)
        assert text_area._highlights == {}
