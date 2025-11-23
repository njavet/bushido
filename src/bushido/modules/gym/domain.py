import datetime
from dataclasses import dataclass
from enum import StrEnum

from bushido.modules.dtypes import UnitData


class GymUnitName(StrEnum):
    weights = "weights"
    martial_arts = "martial_arts"
    yoga = "yoga"


@dataclass
class GymSpec(UnitData):
    start_t: datetime.time
    end_t: datetime.time
    location: str
    training: str | None = None
    focus: str | None = None
