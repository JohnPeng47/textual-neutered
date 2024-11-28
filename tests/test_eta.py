from textual.eta import ETA


def test_get_progress_at() -> None:
    eta = ETA()
    eta.add_sample(1, 2)
    # Check interpolation works
    assert eta._get_progress_at(0) == (0, 0)
    assert eta._get_progress_at(0.1) == (0.1, 0.2)
    assert eta._get_progress_at(0.5) == (0.5, 1.0)


def test_eta():
    eta = ETA(estimation_period=2, extrapolate_period=5)
    eta.add_sample(1, 0.1)
    assert eta.speed == 0.1
    assert eta.get_eta(1) == 9
    assert eta.get_eta(2) == 8
    assert eta.get_eta(3) == 7
    assert eta.get_eta(4) == 6
    assert eta.get_eta(5) == 5
    # After 5 seconds (extrapolate_period), eta won't update
    assert eta.get_eta(6) == 4
    assert eta.get_eta(7) == 4
    assert eta.get_eta(8) == 4
