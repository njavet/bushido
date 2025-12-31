import datetime
from dataclasses import dataclass
from enum import StrEnum

from bushido.core.dtypes import UnitData

from .orm import CardioUnit


class CardioUnitName(StrEnum):
    running = "running"
    skipping = "skipping"


@dataclass
class CardioSpec(UnitData):
    start_t: datetime.time
    seconds: float
    location: str
    distance: float | None
    avg_hr: int | None
    max_hr: int | None
    calories: int | None


def format_cardio_unit(unit: CardioUnit) -> str:
    return unit.name
