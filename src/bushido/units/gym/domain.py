import datetime
from dataclasses import dataclass
from enum import StrEnum

from bushido.core.dtypes import UnitData

from .orm import GymUnit

GYM_GRAMMAR = """
<name> <start>-<end> <location> [<training>] [<focus>] # [<comment>]

name:
  weights | martial_arts | yoga

time:
  HHMM-HHMM
"""


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


def format_gym_unit(unit: GymUnit) -> str:
    return unit.name
