import datetime
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ParsedBaseUnit:
    name: str
    tokens: list[str]
    log_time: datetime.datetime
    comment: str | None = None
