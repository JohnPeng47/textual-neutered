from __future__ import annotations

from time import sleep

from textual.notifications import Notification, Notifications


def test_remove_notification_multiple_times() -> None:
    """It should be possible to remove the same notification more than once without an error."""
    tester = Notifications()
    alert = Notification("delete me")
    tester.add(alert)
    assert list(tester) == [alert]
    del tester[alert]
    assert list(tester) == []
    del tester[alert]
    assert list(tester) == []


def test_clear() -> None:
    """It should be possible to clear all notifications."""
    tester = Notifications()
    for _ in range(100):
        tester.add(Notification("test", timeout=120))
    assert len(tester) == 100
    tester.clear()
    assert len(tester) == 0
