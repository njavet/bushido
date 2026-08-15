from collections.abc import Callable, Iterable
from dataclasses import replace

from ._spec import LiftingData, LiftingSetData, LiftingUnit


def compute_unit_pr(
    units: Iterable[LiftingUnit],
    n: int,
    key_fn: Callable[[tuple[LiftingUnit, LiftingSetData]], tuple[float, float]],
) -> list[LiftingUnit]:
    candidates = [(unit, set_) for unit in units for set_ in unit.data.sets]
    best = sorted(
        candidates,
        key=key_fn,
        reverse=True,
    )[:n]
    return [replace(unit, data=replace(unit.data, sets=[set_])) for unit, set_ in best]


class HeaviestSetMetric:
    def compute(self, units: Iterable[LiftingUnit]) -> list[LiftingUnit]:
        return compute_unit_pr(units, n=3, key_fn=lambda x: (x[1].weight, x[1].reps))


class MostRepsSetMetric:
    def compute(self, units: Iterable[LiftingUnit]) -> list[LiftingUnit]:
        return compute_unit_pr(units, n=3, key_fn=lambda x: (x[1].reps, x[1].weight))
