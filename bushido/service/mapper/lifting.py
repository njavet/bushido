# project imports
from bushido.domain.base import ParsedUnit
from bushido.db import Exercise, LiftingSet
from bushido.service.mapper.base import UnitMapper


class LiftingMapper(UnitMapper):
    def to_orm(self, parsed_unit: ParsedUnit
    ) -> list[ORM_T]: ...

    def from_orm(self, orm_lst: list[ORM_T]) -> ParsedUnit: ...
