from __future__ import annotations

from time import sleep

from textual.notifications import Notification


def test_identity_is_unique() -> None:
    """A collection of notifications should, by default, have unique IDs."""
    notifications: set[str] = set()
    for _ in range(1000):
        notifications.add(Notification("test").identity)
    assert len(notifications) == 1000


def test_time_out() -> None:
    test = Notification("test", timeout=0.5)
    assert test.has_expired is False
    sleep(0.6)
    assert test.has_expired is True
