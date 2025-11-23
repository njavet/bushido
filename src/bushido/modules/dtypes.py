import datetime
from dataclasses import dataclass
from typing import Generic, Literal, Protocol, TypeAlias, TypeVar

from .orm import Unit


class UnitData(Protocol): ...


class Subunit(Protocol):
    # TODO vs abstract orm class
    id: int
    fk_unit: int


T = TypeVar("T")
TUData = TypeVar("TUData", bound=UnitData, covariant=True)
TU = TypeVar("TU", bound=Unit, covariant=True)
TS = TypeVar("TS", bound=Subunit, covariant=True)


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[TUData]):
    name: str
    data: TUData
    comment: str | None = None
    log_dt: datetime.datetime | None = None


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
