from dataclasses import dataclass
from enum import StrEnum

from bushido.core.dtypes import UnitData

from .orm import LiftingSet, LiftingUnit


class LiftingUnitName(StrEnum):
    squat = "squat"
    deadlift = "deadlift"
    benchpress = "benchpress"
    overheadpress = "overheadpress"
    rows = "rows"
    curls = "curls"


@dataclass(frozen=True, slots=True)
class SetSpec:
    set_nr: int
    weight: float
    reps: float
    rest: float


@dataclass(frozen=True, slots=True)
class LiftingSpec(UnitData):
    sets: list[SetSpec]


def format_lifting_unit(unit: LiftingUnit) -> str:
    def format_set(s: LiftingSet) -> str:
        if s.weight == int(s.weight):
            weight = str(int(s.weight))
        else:
            weight = str(s.weight)
        if s.reps == int(s.reps):
            reps = str(int(s.reps))
        else:
            reps = str(s.reps)
        if s.rest == 0:
            return " ".join([weight, reps])
        else:
            return " ".join([weight, reps, str(int(s.rest)), ", "])

    return "".join(map(format_set, unit.subunits))
