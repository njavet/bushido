from typing import override

from citadel.domain.unit import LiftingUnit, UnitType

from ..models import LiftingUnitTable, UnitTable
from ._base import BaseUnitRepo


class LiftingUnitRepo(BaseUnitRepo[LiftingUnit]):
    unit_type = UnitType.lifting

    @override
    def add_unit(self, unit: LiftingUnit, spartan_id: int) -> None:
        orm_unit = UnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            lifting=LiftingUnitTable(
                start_t=unit.start_t,
                end_t=unit.end_t,
                gym=unit.gym,
            ),
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: UnitTable) -> LiftingUnit:
        assert orm_unit.lifting is not None
        return LiftingUnit(
            name=orm_unit.name,
            start_t=orm_unit.lifting.start_t,
            end_t=orm_unit.lifting.end_t,
            gym=orm_unit.lifting.gym,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
