from typing import Protocol

# project imports
from bushido.core.types import ORM_ST, ORM_T, UNIT_T
from bushido.domain.unit import ParsedUnit


class UnitMapper(Protocol[UNIT_T, ORM_T, ORM_ST]):
    def to_orm(
        self, parsed_unit: ParsedUnit[UNIT_T]
    ) -> tuple[ORM_T, list[ORM_ST]]: ...

    def from_orm(
        self, orms: tuple[ORM_T, list[ORM_ST]]
    ) -> ParsedUnit[UNIT_T]: ...
