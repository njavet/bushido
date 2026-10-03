from typing import override

from citadel.domain.unit.lifting import LiftingUnit

from ..models import LiftingUnitTable
from ._base import BaseUnitRepo


class LiftingUnitRepo(BaseUnitRepo[LiftingUnit, LiftingUnitTable]):
    orm_cls = LiftingUnitTable

    @override
    def _to_orm(self, unit: LiftingUnit) -> LiftingUnitTable:
        return LiftingUnitTable(
            name=unit.name,
            log_time=unit.log_time,
            start_t=unit.start_t,
            end_t=unit.end_t,
            gym=unit.gym,
            comment=unit.comment,
        )

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
