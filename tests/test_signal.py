import pytest

from textual.app import App, ComposeResult
from textual.signal import Signal, SignalError
from textual.widgets import Label


def test_repr():
    """Check the repr doesn't break."""
    app = App()
    test_signal = Signal(app, "test")
    assert isinstance(repr(test_signal), str)


async def test_signal_parameters():
    str_result: str | None = None
    int_result: int | None = None

    class TestApp(App):
        BINDINGS = [("space", "signal")]

        def __init__(self) -> None:
            self.str_signal: Signal[str] = Signal(self, "str")
            self.int_signal: Signal[int] = Signal(self, "int")
            super().__init__()

        def action_signal(self) -> None:
            self.str_signal.publish("foo")
            self.int_signal.publish(3)

        def on_mount(self) -> None:
            def on_str(my_str):
                nonlocal str_result
                str_result = my_str

            def on_int(my_int):
                nonlocal int_result
                int_result = my_int

            self.str_signal.subscribe(self, on_str)
            self.int_signal.subscribe(self, on_int)

    app = TestApp()
    async with app.run_test() as pilot:
        await pilot.press("space")
        assert str_result == "foo"
        assert int_result == 3
