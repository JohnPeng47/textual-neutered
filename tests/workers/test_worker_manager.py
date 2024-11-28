import asyncio
import time

from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.worker import Worker, WorkerState


async def test_run_worker_thread_non_async() -> None:
    """Check self.run_worker"""
    worker_events: list[Worker.StateChanged] = []

    work_result: str = ""

    class WorkerWidget(Widget):
        def work(self) -> str:
            nonlocal work_result
            time.sleep(0.02)
            work_result = "foo"
            return "foo"

        def on_mount(self):
            self.run_worker(self.work, thread=True)

        def on_worker_state_changed(self, event) -> None:
            worker_events.append(event)

    class WorkerApp(App):
        def compose(self) -> ComposeResult:
            yield WorkerWidget()

    app = WorkerApp()
    async with app.run_test():
        await app.workers.wait_for_complete()

    assert work_result == "foo"
    assert isinstance(worker_events[0].worker.node, WorkerWidget)
    states = [event.state for event in worker_events]
    assert states == [
        WorkerState.PENDING,
        WorkerState.RUNNING,
        WorkerState.SUCCESS,
    ]


async def test_run_worker_thread_async() -> None:
    """Check self.run_worker"""
    worker_events: list[Worker.StateChanged] = []

    work_result: str = ""

    class WorkerWidget(Widget):
        async def work(self) -> str:
            nonlocal work_result
            time.sleep(0.02)
            work_result = "foo"
            return "foo"

        def on_mount(self):
            self.run_worker(self.work, thread=True)

        def on_worker_state_changed(self, event) -> None:
            worker_events.append(event)

    class WorkerApp(App):
        def compose(self) -> ComposeResult:
            yield WorkerWidget()

    app = WorkerApp()
    async with app.run_test():
        await app.workers.wait_for_complete()

    assert work_result == "foo"
    assert isinstance(worker_events[0].worker.node, WorkerWidget)
    states = [event.state for event in worker_events]
    assert states == [
        WorkerState.PENDING,
        WorkerState.RUNNING,
        WorkerState.SUCCESS,
    ]
