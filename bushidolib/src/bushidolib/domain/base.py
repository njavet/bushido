import datetime
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeVar

T = TypeVar("T")


class UnitCategory(StrEnum):
    CARDIO = "cardio"
    GYM = "gym"
    LIFTING = "lifting"
    WIMHOF = "wimhof"


@dataclass(frozen=True, slots=True)
class UnitSetting:
    name: str
    category: UnitCategory


@dataclass(frozen=True, slots=True)
class Unit[T]:
    name: str
    log_time: datetime.datetime
    comment: str | None
    data: T
