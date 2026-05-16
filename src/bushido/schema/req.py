import datetime

from pydantic import BaseModel


class UnitLogRequest(BaseModel):
    name: str
    tokens: tuple[str, ...]
    log_time: datetime.datetime
    comment: str | None = None
