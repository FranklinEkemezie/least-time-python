import math

import numpy as np

from least_time.models.geometry import Point
from least_time.mathematics.travel_time import angles_from_crossing_point, travel_time, travel_time_derivative


def test_travel_time_matches_definition() -> None:
    saver, savee = Point(-4, 4), Point(5, -3)
    expected = math.hypot(4, 4) / 4 + math.hypot(5, 3) / 2
    assert math.isclose(travel_time(0, saver, savee, 4, 2), expected)


def test_travel_time_vectorizes() -> None:
    values = travel_time(np.array([-1.0, 0.0, 1.0]), Point(-4, 4), Point(5, -3), 4, 2)
    assert values.shape == (3,)
    assert values[1] > 0


def test_derivative_is_zero_for_symmetric_equal_speed_case() -> None:
    saver, savee = Point(-3, 4), Point(3, -4)
    assert abs(travel_time_derivative(0, saver, savee, 2, 2)) < 1e-12


def test_angles_are_relative_to_normal() -> None:
    theta1, theta2 = angles_from_crossing_point(0, Point(-3, 4), Point(3, -4))
    assert math.isclose(theta1, math.atan(3 / 4))
    assert math.isclose(theta2, math.atan(3 / 4))
