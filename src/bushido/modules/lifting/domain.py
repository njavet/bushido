from dataclasses import dataclass
from enum import StrEnum

from bushido.modules.domain import UnitData


class LiftingUnitName(StrEnum):
    squat = "squat"
    deadlift = "deadlift"
    benchpress = "benchpress"
    overheadpress = "overheadpress"
    rows = "rows"
    curls = "curls"


@dataclass(frozen=True, slots=True)
class SetSpec(UnitData):
    set_nr: int
    weight: float
    reps: float
    rest: float
