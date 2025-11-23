from typing import Protocol

from bushido.modules.domain import ParsedUnit, UnitData
from bushido.modules.repo import S, U


class UnitMapper(Protocol[UnitData, U, S]):
    def to_orm(self, parsed_unit: ParsedUnit[UnitData]) -> tuple[U, list[S]]: ...

    def from_orm(self, orms: tuple[U, list[S]]) -> ParsedUnit[UnitData]: ...
