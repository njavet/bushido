import datetime
from enum import StrEnum

from pydantic import BaseModel


class UnitType(StrEnum):
    swimming = "swimming"
    running = "running"
    skipping = "skipping"
    chrono = "chrono"
    log = "log"
    martial_arts = "martial_arts"
    lifting = "lifting"
    bilateral = "bilateral"
    unilateral = "unilateral"
    wimhof = "wimhof"
    work = "work"
    blood_pressure = "blood_pressure"
    scale = "scale"
    tape = "tape"


class BaseUnit(BaseModel):
    name: str
    log_time: datetime.datetime
    comment: str | None = None


class SpaceTimeData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
