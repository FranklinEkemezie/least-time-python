from __future__ import annotations

import numpy as np

from least_time.models.geometry import Point, distance


def _as_array(x: float | np.ndarray) -> float | np.ndarray:
    return np.asarray(x, dtype=float) if isinstance(x, np.ndarray) else float(x)


def travel_time(x: float | np.ndarray, saver: Point, savee: Point, v1: float, v2: float) -> float | np.ndarray:
    """Compute time through Region 1 and Region 2 for interface coordinate(s) ``x``."""

    if v1 <= 0 or v2 <= 0:
        raise ValueError("speeds must be positive")
    values = _as_array(x)
    d1 = np.sqrt((values - saver.x) ** 2 + saver.y**2)
    d2 = np.sqrt((savee.x - values) ** 2 + savee.y**2)
    result = d1 / v1 + d2 / v2
    return float(result) if np.ndim(result) == 0 else result


def travel_time_derivative(x: float, saver: Point, savee: Point, v1: float, v2: float) -> float:
    """Return dT/dx at one interface coordinate."""

    if v1 <= 0 or v2 <= 0:
        raise ValueError("speeds must be positive")
    d1 = np.hypot(x - saver.x, saver.y)
    d2 = np.hypot(x - savee.x, savee.y)
    return (x - saver.x) / (v1 * d1) + (x - savee.x) / (v2 * d2)


def angles_from_crossing_point(x: float, saver: Point, savee: Point) -> tuple[float, float]:
    """Return angles in radians relative to the interface normal."""

    d1 = distance(saver, Point(x, 0.0))
    d2 = distance(savee, Point(x, 0.0))
    return float(np.arcsin(abs(x - saver.x) / d1)), float(np.arcsin(abs(x - savee.x) / d2))

