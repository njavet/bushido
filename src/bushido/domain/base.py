import datetime
from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, Literal, TypeVar

T = TypeVar("T")
UNIT_T = TypeVar("UNIT_T")


class UnitCategory(StrEnum):
    lifting = "lifting"
    gym = "gym"
    wimhof = "wimhof"


@dataclass(frozen=True)
class ParsedUnit(Generic[UNIT_T]):
    name: str
    data: UNIT_T
    comment: str | None = None
    log_dt: datetime.datetime | None = None


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T
    kind: Literal["ok"] = "ok"


@dataclass(frozen=True)
class Warn(Generic[T]):
    value: T
    message: str
    kind: Literal["warning"] = "warning"


@dataclass(frozen=True)
class Err:
    message: str
    kind: Literal["err"] = "err"


Result = Ok[T] | Warn[T] | Err
