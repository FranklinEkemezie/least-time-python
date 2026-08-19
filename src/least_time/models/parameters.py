from __future__ import annotations

from dataclasses import dataclass
import math

from .geometry import Point


@dataclass(frozen=True, slots=True)
class RescueParameters:
    """Validated source parameters for the two-region rescue problem."""

    saver: Point
    savee: Point
    v1: float
    v2: float
    crossing_x: float
    x_min: float = -10.0
    x_max: float = 10.0

    def __post_init__(self) -> None:
        if self.saver.y <= 0:
            raise ValueError("the saver must be in Region 1 (y > 0)")
        if self.savee.y >= 0:
            raise ValueError("the savee must be in Region 2 (y < 0)")
        if not math.isfinite(self.v1) or self.v1 <= 0:
            raise ValueError("v1 must be positive")
        if not math.isfinite(self.v2) or self.v2 <= 0:
            raise ValueError("v2 must be positive")
        if not self.x_min < self.x_max:
            raise ValueError("x_min must be less than x_max")
        if not self.x_min <= self.crossing_x <= self.x_max:
            raise ValueError("crossing_x must lie within the interface bounds")

    @classmethod
    def from_values(cls, *, saver_x: float, saver_y: float, savee_x: float, savee_y: float,
                    v1: float, v2: float, crossing_x: float,
                    x_min: float = -10.0, x_max: float = 10.0) -> "RescueParameters":
        return cls(Point(saver_x, saver_y), Point(savee_x, savee_y), v1, v2,
                   crossing_x, x_min, x_max)


DEFAULT_PARAMETERS = RescueParameters.from_values(
    saver_x=-4.0, saver_y=4.0, savee_x=5.0, savee_y=-3.0,
    v1=4.0, v2=2.0, crossing_x=0.0,
)

