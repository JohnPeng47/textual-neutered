import pytest

from textual.widgets.text_area import Document

TEXT = """I must not fear.
Fear is the mind-killer."""

TEXT_NEWLINE = TEXT + "\n"
TEXT_WINDOWS = TEXT.replace("\n", "\r\n")
TEXT_WINDOWS_NEWLINE = TEXT_NEWLINE.replace("\n", "\r\n")


@pytest.mark.parametrize(
    "text", [TEXT, TEXT_NEWLINE, TEXT_WINDOWS, TEXT_WINDOWS_NEWLINE]
)
def test_location_from_index(text):
    document = Document(text)
    lines = text.split(document.newline)
    assert document.get_location_from_index(0) == (0, 0)
    assert document.get_location_from_index(len(lines[0])) == (0, len(lines[0]))
    if len(document.newline) > 1:
        assert document.get_location_from_index(len(lines[0]) + 1) == (
            0,
            len(lines[0]) + 1,
        )
    assert document.get_location_from_index(len(lines[0]) + len(document.newline)) == (
        1,
        0,
    )
    assert document.get_location_from_index(len(text)) == (
        len(lines) - 1,
        len(lines[-1]),
    )


@pytest.mark.parametrize(
    "text", [TEXT, TEXT_NEWLINE, TEXT_WINDOWS, TEXT_WINDOWS_NEWLINE]
)
def test_document_end(text):
    """The location is always what we expect."""
    document = Document(text)
    expected_line_number = (
        len(text.splitlines()) if text.endswith("\n") else len(text.splitlines()) - 1
    )
    expected_pos = 0 if text.endswith("\n") else (len(text.splitlines()[-1]))
    assert document.end == (expected_line_number, expected_pos)
