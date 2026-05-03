from typing import Protocol, TypeVar

from bushido.core.dtypes import ParsedUnit, UnitData
from bushido.units.orm import Subunit, Unit

TU = TypeVar("TU", bound=Unit)
TS = TypeVar("TS", bound=Subunit)


class UnitMapper(Protocol[T, TU, TS]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[UnitData]) -> tuple[TU, list[TS]]: ...

    @staticmethod
    def from_orm(orms: tuple[TU, list[TS]]) -> ParsedUnit[UnitData]: ...
