from typing import Protocol

from bushido.core.types import ORM_T, UNIT_T
from bushido.domain.unit import ParsedUnit
from bushido.infra.db import Unit


# TODO check types
class UnitMapper(Protocol[UNIT_T, ORM_T]):
    def to_orm(
        self, parsed_unit: ParsedUnit[UNIT_T]
    ) -> tuple[Unit, list[ORM_T]]: ...

    def from_orm(
        self, orms: tuple[Unit, list[ORM_T]]
    ) -> ParsedUnit[UNIT_T]: ...
