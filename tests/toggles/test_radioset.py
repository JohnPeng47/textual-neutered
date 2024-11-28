from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import RadioButton, RadioSet


class RadioSetApp(App[None]):
    def __init__(self):
        super().__init__()
        self.events_received = []

    def compose(self) -> ComposeResult:
        with RadioSet(id="from_buttons"):
            yield RadioButton(id="clickme")
            yield RadioButton()
            yield RadioButton(value=True)
        yield RadioSet("One", "True", "Three", id="from_strings")

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        assert event.radio_set is event.control
        self.events_received.append(
            (
                event.radio_set.id,
                event.index,
                [button.value for button in event.radio_set.query(RadioButton)],
            )
        )


class BadRadioSetApp(App[None]):
    def compose(self) -> ComposeResult:
        with RadioSet():
            for n in range(20):
                yield RadioButton(str(n), True)


async def test_there_can_only_be_one():
    """Adding multiple 'on' buttons should result in only one on."""
    async with BadRadioSetApp().run_test() as pilot:
        assert len(pilot.app.query("RadioButton.-on")) == 1
        assert pilot.app.query_one(RadioSet).pressed_index == 0


class RadioSetDisabledButtonsApp(App[None]):
    def compose(self) -> ComposeResult:
        self.selected = []
        with RadioSet():
            yield RadioButton("0", disabled=True)
            yield RadioButton("1")
            yield RadioButton("2", disabled=True)
            yield RadioButton("3", disabled=True)
            yield RadioButton("4")
            yield RadioButton("5")
            yield RadioButton("6", disabled=True)
            yield RadioButton("7")
            yield RadioButton("8", disabled=True)

    def on_radio_set_changed(self, radio_set: RadioSet.Changed) -> None:
        self.selected.append(str(radio_set.pressed.label))


async def test_keyboard_navigation_with_disabled_buttons():
    """Regression test for https://github.com/Textualize/textual/issues/3839."""

    app = RadioSetDisabledButtonsApp()
    async with app.run_test() as pilot:
        await pilot.press("enter")
        for _ in range(5):
            await pilot.press("down")
            await pilot.press("enter")
        for _ in range(5):
            await pilot.press("up")
            await pilot.press("enter")

    assert app.selected == [
        "1",
        "4",
        "5",
        "7",
        "1",
        "4",
        "1",
        "7",
        "5",
        "4",
        "1",
    ]
