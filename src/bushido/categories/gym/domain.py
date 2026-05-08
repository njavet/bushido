import datetime
from dataclasses import dataclass
from enum import StrEnum

from ..dtypes import ParsedUnit


class GymUnitName(StrEnum):
    martial_arts = "martial_arts"
    weights = "weights"


@dataclass(frozen=True, slots=True)
class GymSpec:
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = None
    focus: str | None = None


@dataclass(frozen=True, slots=True)
class GymUnit(ParsedUnit[GymSpec]):
    pass
