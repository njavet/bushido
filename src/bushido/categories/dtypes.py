import datetime
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

T = TypeVar("T")
P = TypeVar("P", covariant=True)


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...


@dataclass(frozen=True, slots=True)
class SystemClock:
    timezone: datetime.tzinfo = datetime.UTC

    def now(self) -> datetime.datetime:
        return datetime.datetime.now(self.timezone)


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[T]):
    name: str
    data: T
    log_time: datetime.datetime
    comment: str | None = None


@dataclass(frozen=True, slots=True)
class RawUnit:
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None


class UnitParser(Protocol[P]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> P: ...


@dataclass(frozen=True, slots=True)
class CategoryHelp:
    name: str
    grammar: str
    unit_names: list[str]
