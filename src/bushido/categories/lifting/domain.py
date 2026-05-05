from dataclasses import dataclass
from enum import StrEnum

from ..dtypes import ParsedUnit


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
class LiftingSpec:
    sets: list[SetSpec]


@dataclass(frozen=True, slots=True)
class LiftingUnit(ParsedUnit[LiftingSpec]):
    pass
