from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar

from least_time.models.geometry import Point, distance
from least_time.models.parameters import RescueParameters
from least_time.models.result import RescueSolution
from .travel_time import angles_from_crossing_point, travel_time, travel_time_derivative


def _bounded_minimum(function, x_min: float, x_max: float) -> float:
    result = minimize_scalar(function, bounds=(x_min, x_max), method="bounded",
                             options={"xatol": 1e-11, "maxiter": 500})
    candidates = [(float(result.x), float(result.fun)),
                  (x_min, float(function(x_min))), (x_max, float(function(x_max)))]
    return min(candidates, key=lambda item: item[1])[0]


def find_optimal_crossing_point(saver: Point, savee: Point, v1: float, v2: float,
                                x_min: float = -10.0, x_max: float = 10.0) -> float:
    """Find the bounded crossing coordinate minimizing total travel time."""

    if not x_min < x_max:
        raise ValueError("x_min must be less than x_max")
    return _bounded_minimum(lambda x: travel_time(x, saver, savee, v1, v2), x_min, x_max)


def solve_rescue(parameters: RescueParameters, curve_points: int = 501) -> tuple[RescueSolution, np.ndarray, np.ndarray]:
    """Solve a rescue state and return derived values plus a vectorized T(x) curve."""

    p = parameters
    optimal_x = find_optimal_crossing_point(p.saver, p.savee, p.v1, p.v2, p.x_min, p.x_max)
    shortest_x = _bounded_minimum(lambda x: distance(p.saver, Point(x, 0)) + distance(p.savee, Point(x, 0)), p.x_min, p.x_max)
    current = float(travel_time(p.crossing_x, p.saver, p.savee, p.v1, p.v2))
    minimum = float(travel_time(optimal_x, p.saver, p.savee, p.v1, p.v2))
    theta1, theta2 = angles_from_crossing_point(optimal_x, p.saver, p.savee)
    solution = RescueSolution(
        crossing=Point(p.crossing_x, 0), current_time=current, optimal_x=optimal_x,
        minimum_time=minimum, derivative_at_optimum=travel_time_derivative(optimal_x, p.saver, p.savee, p.v1, p.v2),
        theta1=theta1, theta2=theta2, shortest_x=shortest_x,
        shortest_distance=float(distance(p.saver, Point(shortest_x, 0)) + distance(p.savee, Point(shortest_x, 0))),
        fastest_distance=float(distance(p.saver, Point(optimal_x, 0)) + distance(p.savee, Point(optimal_x, 0))),
    )
    xs = np.linspace(p.x_min, p.x_max, max(51, curve_points))
    return solution, xs, np.asarray(travel_time(xs, p.saver, p.savee, p.v1, p.v2))

