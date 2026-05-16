from dataclasses import replace
from typing import Callable, Iterable

from ..base import Unit
from .unit import Data, SetData


def compute_unit_pr(
    units: Iterable[Unit[Data]],
    n: int,
    key_fn: Callable[[tuple[Unit[Data], SetData]], tuple[float, float]],
) -> list[Unit[Data]]:
    candidates = [(unit, set_) for unit in units for set_ in unit.data.sets]
    best = sorted(
        candidates,
        key=key_fn,
        reverse=True,
    )[:n]
    return [replace(unit, data=replace(unit.data, sets=[set_])) for unit, set_ in best]


class HeaviestSetMetric:
    def compute(self, units: Iterable[Unit[Data]]) -> list[Unit[Data]]:
        return compute_unit_pr(units, n=3, key_fn=lambda x: (x[1].weight, x[1].reps))


class MostRepsSetMetric:
    def compute(self, units: Iterable[Unit[Data]]) -> list[Unit[Data]]:
        return compute_unit_pr(units, n=3, key_fn=lambda x: (x[1].reps, x[1].weight))
