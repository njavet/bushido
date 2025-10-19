from dataclasses import dataclass
from enum import StrEnum


class LiftingUnitName(StrEnum):
    squat = "squat"
    deadlift = "deadlift"
    benchpress = "benchpress"
    overheadpress = "overheadpress"
    rows = "rows"


@dataclass
class SetSpec:
    set_nr: int
    weight: float
    reps: float
    rest: float


@dataclass
class ExerciseSpec:
    sets: list[SetSpec]
