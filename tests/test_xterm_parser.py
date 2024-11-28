import itertools

import pytest

from textual._xterm_parser import XTermParser
from textual.events import (
    Key,
    MouseDown,
    MouseMove,
    MouseScrollDown,
    MouseScrollUp,
    MouseUp,
    Paste,
)
from textual.messages import TerminalSupportsSynchronizedOutput


def chunks(data, size):
    if size == 0:
        yield data
        return

    chunk_start = 0
    chunk_end = size
    while True:
        yield data[chunk_start:chunk_end]
        chunk_start = chunk_end
        chunk_end += size
        if chunk_end >= len(data):
            yield data[chunk_start:chunk_end]
            break


@pytest.fixture
def parser():
    return XTermParser()


def test_terminal_mode_reporting_synchronized_output_supported(parser):
    sequence = "\x1b[?2026;1$y"
    events = list(parser.feed(sequence))
    assert len(events) == 1
    assert isinstance(events[0], TerminalSupportsSynchronizedOutput)


def test_terminal_mode_reporting_synchronized_output_not_supported(parser):
    sequence = "\x1b[?2026;0$y"
    events = list(parser.feed(sequence))
    assert events == []
