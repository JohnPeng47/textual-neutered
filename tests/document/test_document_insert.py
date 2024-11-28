from textual.widgets.text_area import Document

TEXT = """I must not fear.
Fear is the mind-killer."""


def test_insert_range_text_no_newlines():
    """Ensuring we can do a simple replacement of text."""
    document = Document(TEXT)
    document.replace_range((0, 2), (0, 6), "MUST")
    assert document.lines == [
        "I MUST not fear.",
        "Fear is the mind-killer.",
    ]


TEXT_NEWLINE_EOF = """\
I must not fear.
Fear is the mind-killer.
"""


def test_newline_eof():
    document = Document(TEXT_NEWLINE_EOF)
    assert document.lines == [
        "I must not fear.",
        "Fear is the mind-killer.",
        "",
    ]
