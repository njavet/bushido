import datetime

from pydantic import BaseModel


class BaseUnit(BaseModel):
    name: str
    log_time: datetime.datetime
    comment: str | None = None


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None
