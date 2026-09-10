import datetime

from pydantic import BaseModel

from ..base import BaseUnit


class GymData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str


class GymUnit(BaseUnit):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
