from typing import Protocol, TypeVar

from bushido.core.dtypes import ParsedUnit, TUData
from bushido.modules.orm import Subunit, Unit

TU = TypeVar("TU", bound=Unit)
TS = TypeVar("TS", bound=Subunit)


class UnitMapper(Protocol[TUData, TU, TS]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[TUData]) -> tuple[TU, list[TS]]: ...

    @staticmethod
    def from_orm(orms: tuple[TU, list[TS]]) -> ParsedUnit[TUData]: ...
