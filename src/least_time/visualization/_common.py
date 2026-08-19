from __future__ import annotations

import numpy as np

from least_time.models.geometry import Point


def angle_arc(x: float, point: Point, radius: float, side: str, samples: int = 30) -> tuple[np.ndarray, np.ndarray]:
    """Create a small arc from the upward/downward normal toward a path."""

    dx = point.x - x
    base = np.pi / 2 if side == "top" else -np.pi / 2
    path_angle = np.arctan2(point.y, dx)
    angles = np.linspace(base, path_angle, samples)
    return x + radius * np.cos(angles), radius * np.sin(angles)

