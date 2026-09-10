import datetime

from pydantic import BaseModel


class GymData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = None
    focus: str | None = None
