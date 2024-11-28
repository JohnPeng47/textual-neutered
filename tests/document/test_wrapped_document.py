import pytest

from textual.document._document import Document
from textual.document._wrapped_document import WrappedDocument
from textual.geometry import Offset

SIMPLE_TEXT = "123 4567\n12345\n123456789\n"


def test_get_offsets_no_wrapping():
    document = Document("abc")
    wrapped_document = WrappedDocument(document, width=4)

    assert wrapped_document.get_offsets(0) == []


@pytest.mark.parametrize("line_index", [-4, 10000])
def test_get_offsets_invalid_line_index(line_index):
    document = Document(SIMPLE_TEXT)
    wrapped_document = WrappedDocument(document, width=4)

    with pytest.raises(ValueError):
        wrapped_document.get_offsets(line_index)
