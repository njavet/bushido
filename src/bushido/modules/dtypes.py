import datetime
from dataclasses import dataclass
from typing import Generic, Literal, Protocol, TypeAlias, TypeVar

from bushido.modules.orm import Subunit, Unit


class UnitData(Protocol): ...


T = TypeVar("T")
TUData = TypeVar("TUData", bound=UnitData)
TU = TypeVar("TU", bound=Unit)
TS = TypeVar("TS", bound=Subunit)


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[TUData]):
    name: str
    data: TUData
    comment: str | None = None
    payload: str | None = None
    log_time: datetime.datetime | None = None


@dataclass(frozen=True, slots=True)
class DisplayUnit:
    name: str
    log_time: datetime.datetime
    payload: str | None


@dataclass(frozen=True, slots=True)
class Ok(Generic[T]):
    value: T
    kind: Literal["ok"] = "ok"


@dataclass(frozen=True, slots=True)
class Warn(Generic[T]):
    value: T
    message: str
    kind: Literal["warning"] = "warning"


@dataclass(frozen=True, slots=True)
class Err:
    message: str
    kind: Literal["err"] = "err"


Result: TypeAlias = Ok[T] | Warn[T] | Err


class UnitMapper(Protocol[TUData, TU, TS]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[TUData]) -> tuple[TU, list[TS]]: ...

    @staticmethod
    def from_orm(orms: tuple[TU, list[TS]]) -> ParsedUnit[TUData]: ...
