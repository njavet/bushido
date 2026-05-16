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


def heaviest_lifting_unit_or_none(
    units: Iterable[Unit[LiftingData]],
) -> Unit[LiftingData] | None:
    candidates = [(unit, set_) for unit in units for set_ in unit.data.sets]

    if not candidates:
        return None

    best_unit, best_set = max(candidates, key=lambda x: (x[1].weight, x[1].reps))

    return replace(best_unit, data=replace(best_unit.data, sets=[best_set]))


def most_reps_lifting_unit_or_none(
    units: Iterable[Unit[LiftingData]],
) -> Unit[LiftingData] | None:
    candidates = [(unit, set_) for unit in units for set_ in unit.data.sets]

    if not candidates:
        return None

    best_unit, best_set = max(candidates, key=lambda x: (x[1].reps, x[1].weight))

    return replace(best_unit, data=replace(best_unit.data, sets=[best_set]))
