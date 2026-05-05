import datetime
from dataclasses import dataclass
from enum import StrEnum

from ..dtypes import ParsedUnit


class CardioUnitName(StrEnum):
    running = "running"
    skipping = "skipping"
    swimming = "swimming"


@dataclass(frozen=True, slots=True)
class CardioSpec:
    start_t: datetime.time
    seconds: float
    location: str
    distance: float | None
    avg_hr: int | None
    max_hr: int | None
    calories: int | None


@dataclass(frozen=True, slots=True)
class CardioUnit(ParsedUnit[CardioSpec]):
    pass
