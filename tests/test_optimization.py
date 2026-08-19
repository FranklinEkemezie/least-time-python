import math

import numpy as np

from least_time.models.geometry import Point
from least_time.models.parameters import RescueParameters
from least_time.mathematics.optimization import find_optimal_crossing_point, solve_rescue
from least_time.mathematics.travel_time import travel_time, travel_time_derivative


def test_equal_velocity_optimum_is_straight_line_intersection() -> None:
    saver, savee = Point(-4, 4), Point(5, -3)
    x = find_optimal_crossing_point(saver, savee, 4, 4)
    expected = (-4 * 3 + 5 * 4) / 7
    assert math.isclose(x, expected, abs_tol=1e-7)


def test_optimum_beats_sampled_crossings() -> None:
    p = RescueParameters.from_values(saver_x=-4, saver_y=4, savee_x=5, savee_y=-3, v1=4, v2=2, crossing_x=0)
    solution, xs, times = solve_rescue(p)
    assert solution.minimum_time <= np.min(times) + 1e-7
    assert all(solution.minimum_time <= travel_time(float(x), p.saver, p.savee, p.v1, p.v2) + 1e-7 for x in np.linspace(-9, 9, 17))
    assert abs(travel_time_derivative(solution.optimal_x, p.saver, p.savee, p.v1, p.v2)) < 1e-7

