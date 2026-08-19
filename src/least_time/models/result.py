from __future__ import annotations

from dataclasses import dataclass

from .geometry import Point


@dataclass(frozen=True, slots=True)
class RescueSolution:
    """Derived quantities for one set of rescue parameters."""

    crossing: Point
    current_time: float
    optimal_x: float
    minimum_time: float
    derivative_at_optimum: float
    theta1: float
    theta2: float
    shortest_x: float
    shortest_distance: float
    fastest_distance: float

