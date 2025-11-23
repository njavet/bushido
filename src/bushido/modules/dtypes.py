import datetime
from dataclasses import dataclass
from typing import Generic, Literal, Protocol, TypeVar

from .orm import Unit


class UnitData(Protocol):
    pass


class Subunit(Protocol):
    id: int
    fk_unit: int


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
class Ok(Generic[TUData]):
    value: ParsedUnit[TUData]
    kind: Literal["ok"] = "ok"


@dataclass(frozen=True, slots=True)
class Warn(Generic[TUData]):
    value: ParsedUnit[TUData]
    message: str
    kind: Literal["warning"] = "warning"


@dataclass(frozen=True, slots=True)
class Err:
    message: str
    kind: Literal["err"] = "err"


Result = Ok[TUData] | Warn[TUData] | Err
