import datetime
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class UnitSetting:
    name: str
    emoji: str


@dataclass(frozen=True, slots=True)
class Unit[T]:
    name: str
    log_time: datetime.datetime
    comment: str | None
    data: T
