from dataclasses import dataclass, replace
from typing import Iterable

from bushido.units.base import Unit


@dataclass(frozen=True, slots=True)
class SetData:
    set_nr: int
    weight: float
    reps: float
    rest: float


@dataclass(frozen=True, slots=True)
class LiftingData:
    variant: str | None
    program: str | None
    sets: list[SetData]


class HeaviestSetMetric:
    def compute(self, units: Iterable[Unit[LiftingData]]) -> list[Unit[LiftingData]]:
        candidates = [(unit, set_) for unit in units for set_ in unit.data.sets]
        best = sorted(
            candidates,
            key=lambda x: (x[1].weight, x[1].reps),
            reverse=True,
        )[:3]
        return [
            replace(unit, data=replace(unit.data, sets=[set_])) for unit, set_ in best
        ]


class MostRepsSetMetric:
    def compute(self, units: Iterable[Unit[LiftingData]]) -> list[Unit[LiftingData]]:
        candidates = [(unit, set_) for unit in units for set_ in unit.data.sets]
        best = sorted(
            candidates,
            key=lambda x: (x[1].reps, x[1].weight),
            reverse=True,
        )[:3]
        return [
            replace(unit, data=replace(unit.data, sets=[set_])) for unit, set_ in best
        ]
