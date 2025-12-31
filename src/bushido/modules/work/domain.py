import datetime
from dataclasses import dataclass
from enum import StrEnum

from bushido.core.dtypes import UnitData

from .orm import WorkUnit


class WorkUnitName(StrEnum):
    risktec = "risktec"
    myself = "myself"


@dataclass
class WorkSpec(UnitData):
    start_t: datetime.time
    end_t: datetime.time
    location: str
    employer: str
    project: str


def format_work_unit(unit: WorkUnit) -> str:
    return unit.name
