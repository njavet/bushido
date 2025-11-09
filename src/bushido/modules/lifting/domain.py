from dataclasses import dataclass
from enum import StrEnum


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
