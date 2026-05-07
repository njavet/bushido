import datetime
from dataclasses import dataclass
from enum import StrEnum

from ..dtypes import ParsedUnit


class GymUnitName(StrEnum):
    martial_arts = "martial_arts"
    weights = "weights"


class TrainingType(StrEnum):
    kyokushin = "kyokushin"
    grappling = "grappling"
    lifting = "lifting"


@dataclass(frozen=True, slots=True)
class GymSpec:
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    intensity: int = 3
    training: TrainingType | None = None
    focus: str | None = None
    private: bool = False


@dataclass(frozen=True, slots=True)
class GymUnit(ParsedUnit[GymSpec]):
    pass
