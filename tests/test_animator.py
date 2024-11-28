from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from textual._animator import Animator, SimpleAnimation
from textual._easing import DEFAULT_EASING, EASING


class Animatable:
    """An animatable object."""

    def __init__(self, value):
        self.value = value

    def blend(self, destination: Animatable, factor: float) -> Animatable:
        return Animatable(self.value + (destination.value - self.value) * factor)


@dataclass
class AnimateTest:
    """An object with animatable properties."""

    foo: float | None = 0.0  # Plain float that may be set to None on final_value
    bar: Animatable = Animatable(0)  # A mock object supporting the animatable protocol


class MockAnimator(Animator):
    """A mock animator."""

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self._time = 0.0
        self._on_animation_frame_called = False

    def on_animation_frame(self):
        self._on_animation_frame_called = True

    def _get_time(self):
        return self._time


async def test_animator_on_complete_callback_fired_at_duration():
    callback = Mock()
    animate_test = AnimateTest()
    mock_app = Mock()
    animator = MockAnimator(mock_app)

    animator.animate(animate_test, "foo", 200, duration=10, on_complete=callback)

    animator._time = 10
    animator()

    # Ensure that the callback is scheduled to run after the duration is up.
    mock_app.call_later.assert_called_once_with(callback)


def test_force_stop_animation():
    callback = Mock()
    animate_test = AnimateTest()
    mock_app = Mock()
    animator = MockAnimator(mock_app)

    animator.animate(animate_test, "foo", 200, duration=10, on_complete=callback)

    assert animator.is_being_animated(animate_test, "foo")
    assert animate_test.foo != 200

    animator.force_stop_animation(animate_test, "foo")

    # The animation of the attribute was force cancelled.
    assert not animator.is_being_animated(animate_test, "foo")
    assert animate_test.foo == 200

    # The on_complete callback was scheduled.
    mock_app.call_later.assert_called_once_with(callback)
