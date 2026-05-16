from dataclasses import dataclass
from typing import Iterable

from bushido.units.base import Unit

from ._metrics import compute_unit_pr


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
        key_fn = lambda x: (x[1].weight, x[1].reps)
        return compute_unit_pr(units, n=3, key_fn=key_fn)


class MostRepsSetMetric:
    def compute(self, units: Iterable[Unit[LiftingData]]) -> list[Unit[LiftingData]]:
        key_fn = lambda x: (x[1].reps, x[1].weight)
        return compute_unit_pr(units, n=3, key_fn=key_fn)
