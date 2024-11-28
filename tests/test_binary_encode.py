import pytest

from textual._binary_encode import DecodeError, dump, load


@pytest.mark.parametrize(
    "data",
    [
        set(),
        float,
        ...,
        [float],
    ],
)
def test_dump_invalid_type(data):
    with pytest.raises(TypeError):
        dump(data)


def test_load_wrong_type():
    with pytest.raises(TypeError):
        load(None)
    with pytest.raises(TypeError):
        load("foo")
