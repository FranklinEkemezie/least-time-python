from __future__ import annotations


def normalized_indices(v1: float, v2: float) -> tuple[float, float]:
    """Return indices normalized so Region 1 has index 1.

    Since n=c/v, only the ratio matters for the rescue analogy.
    """

    if v1 <= 0 or v2 <= 0:
        raise ValueError("speeds must be positive")
    return 1.0, v1 / v2


def refractive_index_ratio(v1: float, v2: float) -> float:
    """Return n2/n1 = v1/v2."""

    return normalized_indices(v1, v2)[1]


def snell_residual(theta1: float, theta2: float, v1: float, v2: float) -> float:
    """Residual of the velocity-form Snell relationship."""

    return abs(__import__("math").sin(theta1) / v1 - __import__("math").sin(theta2) / v2)

