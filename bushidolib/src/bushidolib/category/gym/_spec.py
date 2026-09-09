import datetime
from typing import Literal

from pydantic import BaseModel

from bushidolib.constants import UnitCategory
from bushidolib.unit import BaseUnit

grammar = """
    <name> <start>-<end> <location> [<training>] [<focus>] # [<comment>]

    time format:
      HHMM-HHMM
"""


class GymData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = None
    focus: str | None = None


class GymUnit(BaseUnit):
    unit_category: Literal[UnitCategory.GYM] = UnitCategory.GYM
    data: GymData
