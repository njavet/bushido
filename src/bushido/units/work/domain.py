import datetime
from dataclasses import dataclass
from enum import StrEnum

from .orm import WorkUnit


class WorkUnitName(StrEnum):
    risktec = "risktec"
    myself = "myself"


@dataclass(
    frozen=True,
    slots=True,
)
class WorkSpec:
    start_t: datetime.time
    end_t: datetime.time
    location: str
    employer: str
    project: str


def format_work_unit(unit: WorkUnit) -> str:
    return unit.name
