from typing import override

from citadel.unit.strength import LiftingUnit
from citadel.unit.base import UnitType

from ..models import LiftingUnitTable
from ._base import BaseUnitRepo


class LiftingUnitRepo(BaseUnitRepo[LiftingUnit, LiftingUnitTable]):
    orm_cls = LiftingUnitTable
    unit_type = UnitType.lifting

    @override
    def add_unit(self, unit: LiftingUnit, spartan_id: int) -> None:
        orm_unit = LiftingUnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            start_t=unit.start_t,
            end_t=unit.end_t,
            gym=unit.gym,
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: LiftingUnitTable) -> LiftingUnit:
        return LiftingUnit(
            name=orm_unit.name,
            start_t=orm_unit.start_t,
            end_t=orm_unit.end_t,
            gym=orm_unit.gym,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
