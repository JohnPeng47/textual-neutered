from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Button, Label, Static


class ExampleApp(App):
    def compose(self) -> ComposeResult:
        yield Button("ABC")
        yield Label("Outside of vertical.")
        with Vertical():
            for index in range(5):
                yield Label(str(index))


async def test_widget_remove_children_no_children():
    app = ExampleApp()
    async with app.run_test():
        button = app.query_one(Button)

        count_before = len(app.query("*"))
        await button.remove_children()
        count_after = len(app.query("*"))

        assert len(app.query(Button)) == 1  # The button still remains.
        assert (
            count_before == count_after
        )  # No widgets have been removed, since Button has no children.


async def test_widget_remove_children_no_children_match_selector():
    app = ExampleApp()
    async with app.run_test():
        container = app.query_one(Vertical)
        assert len(container.query("Button")) == 0  # Sanity check.

        count_before = len(app.query("*"))
        container_children_before = list(container.children)
        await container.remove_children("Button")

        assert count_before == len(app.query("*"))
        assert container_children_before == list(container.children)
