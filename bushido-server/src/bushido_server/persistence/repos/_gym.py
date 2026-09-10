from typing import override

from bushidolib.category.gym import GymUnit

from ..models import GymUnitTable
from ._base import BaseUnitRepo


class GymUnitRepo(BaseUnitRepo[GymUnit, GymUnitTable]):
    orm_cls = GymUnitTable

    @override
    def _to_orm(self, unit: GymUnit) -> GymUnitTable:
        return GymUnitTable(
            name=unit.name,
            log_time=unit.log_time,
            start_t=unit.start_t,
            end_t=unit.end_t,
            gym=unit.gym,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: GymUnitTable) -> GymUnit:
        return GymUnit(
            name=orm_unit.name,
            start_t=orm_unit.start_t,
            end_t=orm_unit.end_t,
            gym=orm_unit.gym,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
