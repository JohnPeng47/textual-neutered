import pytest

from textual.widgets.text_area import Document, EditResult

TEXT = """I must not fear.
Fear is the mind-killer.
I forgot the rest of the quote.
Sorry Will."""


@pytest.fixture
def document():
    document = Document(TEXT)
    return document


def test_delete_single_line_including_newline(document):
    """Delete from the start of a line to the start of the line below."""
    replace_result = document.replace_range((2, 0), (3, 0), "")
    assert replace_result == EditResult(
        end_location=(2, 0),
        replaced_text="I forgot the rest of the quote.\n",
    )
    assert document.lines == [
        "I must not fear.",
        "Fear is the mind-killer.",
        "Sorry Will.",
    ]


TEXT_NEWLINE_EOF = """\
I must not fear.
Fear is the mind-killer.
"""


def test_delete_end_of_file_newline():
    document = Document(TEXT_NEWLINE_EOF)
    replace_result = document.replace_range((2, 0), (1, 24), "")
    assert replace_result == EditResult(end_location=(1, 24), replaced_text="\n")
    assert document.lines == [
        "I must not fear.",
        "Fear is the mind-killer.",
    ]
