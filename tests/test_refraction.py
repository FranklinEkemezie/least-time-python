import math

from least_time.models.geometry import Point
from least_time.models.parameters import RescueParameters
from least_time.mathematics.optimization import solve_rescue
from least_time.mathematics.refraction import normalized_indices, refractive_index_ratio


def test_velocity_form_of_snell_at_optimum() -> None:
    p = RescueParameters.from_values(saver_x=-4, saver_y=4, savee_x=5, savee_y=-3, v1=4, v2=2, crossing_x=0)
    solution, _, _ = solve_rescue(p)
    assert math.isclose(math.sin(solution.theta1) / p.v1, math.sin(solution.theta2) / p.v2, rel_tol=1e-6, abs_tol=1e-8)


def test_normalized_index_ratio() -> None:
    n1, n2 = normalized_indices(4, 2)
    assert n1 == 1
    assert math.isclose(n2, 2)
    assert math.isclose(refractive_index_ratio(4, 2), 2)


def test_snell_index_form_at_optimum() -> None:
    p = RescueParameters.from_values(saver_x=-4, saver_y=4, savee_x=5, savee_y=-3, v1=4, v2=2, crossing_x=0)
    solution, _, _ = solve_rescue(p)
    n1, n2 = normalized_indices(p.v1, p.v2)
    assert math.isclose(n1 * math.sin(solution.theta1), n2 * math.sin(solution.theta2), rel_tol=1e-6)

