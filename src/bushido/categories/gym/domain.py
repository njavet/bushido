import datetime
from dataclasses import dataclass

from ..dtypes import ParsedUnit


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
