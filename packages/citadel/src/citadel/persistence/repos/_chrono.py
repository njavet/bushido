from typing import override

from citadel.unit.base import UnitType
from citadel.unit.martial_arts import ChronoUnit

from ..models import ChronoUnitTable
from ._base import BaseUnitRepo


class ChronoUnitRepo(BaseUnitRepo[ChronoUnit, ChronoUnitTable]):
    orm_cls = ChronoUnitTable
    unit_type = UnitType.chrono

    @override
    def add_unit(self, unit: ChronoUnit, spartan_id: int) -> None:
        orm_unit = ChronoUnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            seconds=unit.seconds,
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: ChronoUnitTable) -> ChronoUnit:
        return ChronoUnit(
            name=orm_unit.name,
            seconds=orm_unit.seconds,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
