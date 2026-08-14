from typing import override

from bushidolib.domain import Unit
from bushidolib.domain.gym import GymData

from ..models import GymUnitTable
from ._base import BaseUnitRepo


class GymUnitRepo(BaseUnitRepo[GymData, GymUnitTable]):
    orm_cls = GymUnitTable

    @override
    @staticmethod
    def _to_orm(unit: Unit[GymData]) -> GymUnitTable:
        return GymUnitTable(
            name=unit.name,
            log_time=unit.log_time,
            start_t=unit.data.start_t,
            end_t=unit.data.end_t,
            gym=unit.data.gym,
            training=unit.data.training,
            focus=unit.data.focus,
            comment=unit.comment,
        )

    @override
    @staticmethod
    def _from_orm(orm_unit: GymUnitTable) -> Unit[GymData]:
        return Unit(
            name=orm_unit.name,
            data=GymData(
                start_t=orm_unit.start_t,
                end_t=orm_unit.end_t,
                gym=orm_unit.gym,
                training=orm_unit.training,
                focus=orm_unit.focus,
            ),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
