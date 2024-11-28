import asyncio

import pytest

from textual.app import App
from textual.worker import (
    DeadlockError,
    NoActiveWorker,
    Worker,
    WorkerCancelled,
    WorkerError,
    WorkerFailed,
    WorkerState,
    get_current_worker,
)


async def test_self_referential_deadlock():
    async def self_referential_work():
        await get_current_worker().wait()

    app = App()
    with pytest.raises(WorkerFailed) as exc:
        async with app.run_test():
            worker = Worker(app, self_referential_work)
            worker._start(app)
            await worker.wait()
        assert exc.type is DeadlockError


async def test_wait_without_start():
    async def work():
        return

    app = App()
    async with app.run_test():
        worker = Worker(app, work)
        with pytest.raises(WorkerError):
            await worker.wait()
