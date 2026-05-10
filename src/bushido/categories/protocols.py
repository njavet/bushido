import datetime
from typing import Protocol

from bushido.categories.dtypes import P


class UnitParser(Protocol[P]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> P: ...


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...


class TrainingUnit(Protocol):
    name: str
    emoji: str
    date: datetime.datetime
    duration: int
    start_t: datetime.time | None = None
    end_t: datetime.time | None = None
    gym: str | None = None
    comment: str | None = None
