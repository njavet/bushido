from typing import Protocol

from bushido.modules.dtypes import ParsedUnit, TUnitData
from bushido.modules.repo import S, U


class UnitMapper(Protocol[TUnitData, TU, TS]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[TUnitData]) -> tuple[U, list[S]]: ...

    @staticmethod
    def from_orm(orms: tuple[U, list[S]]) -> ParsedUnit[TUnitData]: ...
