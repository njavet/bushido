import datetime
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar


class UnitData(Protocol): ...


TUData = TypeVar("TUData", bound=UnitData)


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[TUData]):
    name: str
    data: TUData
    log_time: datetime.datetime
    comment: str | None = None
