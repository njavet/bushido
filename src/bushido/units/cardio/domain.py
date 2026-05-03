import datetime
from dataclasses import dataclass
from enum import StrEnum

from .orm import CardioUnit


class CardioUnitName(StrEnum):
    running = "running"
    skipping = "skipping"


@dataclass(frozen=True, slots=True)
class CardioSpec:
    start_t: datetime.time
    seconds: float
    location: str
    distance: float | None
    avg_hr: int | None
    max_hr: int | None
    calories: int | None


def format_cardio_unit(unit: CardioUnit) -> str:
    return unit.name
