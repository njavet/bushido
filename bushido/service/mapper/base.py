from typing import Protocol

# project imports
from bushido.core.types import ORM_T, UNIT_T
from bushido.domain.base import ParsedUnit


class UnitMapper(Protocol):
    def to_orm(self, parsed_unit: ParsedUnit[UNIT_T]) -> list[ORM_T]: ...

    def from_orm(self, orm_lst: list[ORM_T]) -> ParsedUnit[UNIT_T]: ...
