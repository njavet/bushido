from typing import override

from bushidolib.unit.cardio import CardioUnit

from ..models import CardioUnitTable
from ._base import BaseUnitRepo


class CardioUnitRepo(BaseUnitRepo[CardioUnit, CardioUnitTable]):
    orm_cls = CardioUnitTable

    @override
    def _to_orm(self, unit: CardioUnit) -> CardioUnitTable:
        return CardioUnitTable(
            name=unit.name,
            log_time=unit.log_time,
            start_t=unit.start_t,
            seconds=unit.seconds,
            gym=unit.gym,
            distance=unit.distance,
            avg_hr=unit.avg_hr,
            max_hr=unit.max_hr,
            calories=unit.calories,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: CardioUnitTable) -> CardioUnit:
        return CardioUnit(
            name=orm_unit.name,
            start_t=orm_unit.start_t,
            seconds=orm_unit.seconds,
            gym=orm_unit.gym,
            distance=orm_unit.distance,
            avg_hr=orm_unit.avg_hr,
            max_hr=orm_unit.max_hr,
            calories=orm_unit.calories,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
