import datetime
from dataclasses import dataclass
from typing import Generic, Iterable, Protocol, TypeVar

T = TypeVar("T")
R = TypeVar("R", covariant=True)


@dataclass(frozen=True, slots=True)
class Unit(Generic[T]):
    name: str
    emoji: str
    log_time: datetime.datetime
    comment: str | None
    data: T


@dataclass(frozen=True, slots=True)
class UnitGrammar:
    pass


class UnitMetric(Protocol[T, R]):
    def compute(self, units: Iterable[Unit[T]]) -> R: ...
