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


class UnitData(Protocol): ...


TUData = TypeVar("TUData", bound=UnitData)


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[TUData]):
    name: str
    data: TUData
    log_time: datetime.datetime
    comment: str | None = None
