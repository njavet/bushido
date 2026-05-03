import datetime
from dataclasses import dataclass
from enum import StrEnum

from .orm import GymUnit


class GymUnitName(StrEnum):
    weights = "weights"
    martial_arts = "martial_arts"
    yoga = "yoga"


@dataclass(frozen=True, slots=True)
class GymSpec:
    start_t: datetime.time
    end_t: datetime.time
    location: str
    training: str | None = None
    focus: str | None = None


def format_gym_unit(unit: GymUnit) -> str:
    return unit.name
