import datetime
from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, Literal, TypeVar

T = TypeVar("T")


class UnitData:
    pass


TUnitData = TypeVar("TUnitData", bound=UnitData, covariant=True)


class UnitCategory(StrEnum):
    lifting = "lifting"
    gym = "gym"
    wimhof = "wimhof"


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[TUnitData]):
    name: str
    data: UnitData
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


Result = Ok[T] | Warn[T] | Err
