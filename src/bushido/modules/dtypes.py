import datetime
from dataclasses import dataclass
from typing import Generic, Literal, TypeVar


class UnitData:
    pass


TUnitData = TypeVar("TUnitData", bound=UnitData, covariant=True)


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[TUnitData]):
    name: str
    data: TUnitData
    comment: str | None = None
    log_dt: datetime.datetime | None = None


@dataclass(frozen=True, slots=True)
class Ok(Generic[TUnitData]):
    value: ParsedUnit[TUnitData]
    kind: Literal["ok"] = "ok"


@dataclass(frozen=True, slots=True)
class Warn(Generic[TUnitData]):
    value: ParsedUnit[TUnitData]
    message: str
    kind: Literal["warning"] = "warning"


@dataclass(frozen=True, slots=True)
class Err:
    message: str
    kind: Literal["err"] = "err"


Result = Ok[TUnitData] | Warn[TUnitData] | Err
