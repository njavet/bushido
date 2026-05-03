import datetime
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...


@dataclass(frozen=True, slots=True)
class SystemClock:
    timezone: datetime.tzinfo = datetime.UTC

    def now(self) -> datetime.datetime:
        return datetime.datetime.now(self.timezone)


@dataclass(frozen=True, slots=True)
class RawUnit:
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None


@dataclass(frozen=True, slots=True)
class Options:
    log_time: datetime.datetime


class UnitData(Protocol): ...


T = TypeVar("T", bound=UnitData)


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[T]):
    name: str
    data: T
    options: Options
    comment: str | None = None
