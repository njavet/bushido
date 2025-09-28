import datetime
from dataclasses import dataclass
from typing import Generic, TypeVar

UNIT_T = TypeVar('UNIT_T')


@dataclass(frozen=True)
class ParsedUnit(Generic[UNIT_T]):
    name: str
    data: UNIT_T
    comment: str | None = None
    log_dt: datetime.datetime | None = None
