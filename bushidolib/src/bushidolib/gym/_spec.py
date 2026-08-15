import datetime

from pydantic import BaseModel

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
    data: GymData
