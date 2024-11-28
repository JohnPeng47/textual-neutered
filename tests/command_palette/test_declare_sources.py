from textual.app import App
from textual.command import CommandPalette, Hit, Hits, Provider
from textual.screen import Screen
from textual.system_commands import SystemCommandsProvider


class ExampleCommandSource(Provider):
    async def search(self, _: str) -> Hits:
        def goes_nowhere_does_nothing() -> None:
            pass

        yield Hit(1, "Hit", goes_nowhere_does_nothing, "Hit")


class AppWithActiveCommandPalette(App[None]):
    def on_mount(self) -> None:
        self.action_command_palette()


class AppWithNoSources(AppWithActiveCommandPalette):
    pass


class AppWithSources(AppWithActiveCommandPalette):
    COMMANDS = {ExampleCommandSource}


class AppWithInitialScreen(App[None]):
    def __init__(self, screen: Screen) -> None:
        super().__init__()
        self._test_screen = screen

    def on_mount(self) -> None:
        self.push_screen(self._test_screen)


class ScreenWithNoSources(Screen[None]):
    def on_mount(self) -> None:
        self.app.action_command_palette()


class ScreenWithSources(ScreenWithNoSources):
    COMMANDS = {ExampleCommandSource}


async def test_screen_command_sources() -> None:
    """Command sources declared on a screen should be in the command palette."""
    async with AppWithInitialScreen(ScreenWithSources()).run_test() as pilot:
        assert isinstance(pilot.app.screen, CommandPalette)
        assert pilot.app.screen._provider_classes == {
            SystemCommandsProvider,
            ExampleCommandSource,
        }


class AnotherCommandSource(ExampleCommandSource):
    pass


class CombinedSourceApp(App[None]):
    COMMANDS = {AnotherCommandSource}

    def on_mount(self) -> None:
        self.push_screen(ScreenWithSources())


async def test_app_and_screen_command_sources_combine() -> None:
    """If an app and the screen have command sources they should combine."""
    async with CombinedSourceApp().run_test() as pilot:
        assert isinstance(pilot.app.screen, CommandPalette)
        assert (
            pilot.app.screen._provider_classes
            == CombinedSourceApp.COMMANDS | ScreenWithSources.COMMANDS
        )
