from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True, slots=True)
class Point:
    """A point in the Cartesian demonstration coordinate system."""

    x: float
    y: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.x) or not math.isfinite(self.y):
            raise ValueError("point coordinates must be finite")


def distance(a: Point, b: Point) -> float:
    """Return Euclidean distance between two points."""

    return math.hypot(a.x - b.x, a.y - b.y)

