import datetime
from dataclasses import dataclass

from ..dtypes import ParsedUnit


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
