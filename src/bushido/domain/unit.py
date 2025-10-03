import datetime
from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, TypeVar

UNIT_T = TypeVar("UNIT_T")


class UnitCategory(StrEnum):
    lifting = "lifting"
    gym = "gym"
    wimhof = "wimhof"


class LiftingUnitName(StrEnum):
    squat = "squat"
    deadlift = "deadlift"
    benchpress = "benchpress"
    overheadpress = "overheadpress"
    rows = "rows"


class GymUnitName(StrEnum):
    weights = "weights"
    martial_arts = "martial_arts"
    yoga = "yoga"


@dataclass(frozen=True)
class ParsedUnit(Generic[UNIT_T]):
    name: str
    data: UNIT_T
    comment: str | None = None
    log_dt: datetime.datetime | None = None
