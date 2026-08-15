import datetime
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Unit[T]:
    name: str
    log_time: datetime.datetime
    comment: str | None
    data: T
