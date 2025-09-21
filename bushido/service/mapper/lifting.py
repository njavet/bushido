# project imports
from bushido.core.types import ORM_T
from bushido.domain.base import ParsedUnit
from bushido.service.mapper.base import UnitMapper


class LiftingMapper(UnitMapper):
    def to_orm(self, parsed_unit: ParsedUnit
    ) -> list[ORM_T]: ...

    def from_orm(self, orm_lst: list[ORM_T]) -> ParsedUnit: ...
