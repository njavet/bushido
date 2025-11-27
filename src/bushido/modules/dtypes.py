import datetime
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

from bushido.modules.orm import Subunit, Unit


class UnitData(Protocol): ...


TUData = TypeVar("TUData", bound=UnitData)
TU = TypeVar("TU", bound=Unit)
TS = TypeVar("TS", bound=Subunit)


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[TUData]):
    name: str
    data: TUData
    log_time: datetime.datetime
    comment: str | None = None


class UnitMapper(Protocol[TUData, TU, TS]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[TUData]) -> tuple[TU, list[TS]]: ...

    @staticmethod
    def from_orm(orms: tuple[TU, list[TS]]) -> ParsedUnit[TUData]: ...
