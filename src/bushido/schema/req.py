import datetime

from pydantic import BaseModel


class LogRequest(BaseModel):
    name: str
    tokens: tuple[str, ...]
    log_time: datetime.datetime
    comment: str | None = None
