import datetime

from pydantic import BaseModel


class BaseUnit(BaseModel):
    log_time: datetime.datetime
    comment: str | None = None


class SpaceTimeData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
