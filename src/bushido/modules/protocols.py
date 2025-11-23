from typing import Protocol

from bushido.modules.dtypes import ParsedUnit, TUnitData
from bushido.modules.repo import S, U


class UnitMapper(Protocol[TUnitData, U, S]):
    def to_orm(self, parsed_unit: ParsedUnit[TUnitData]) -> tuple[U, list[S]]: ...

    def from_orm(self, orms: tuple[U, list[S]]) -> ParsedUnit[TUnitData]: ...
