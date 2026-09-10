from typing import override

from bushidolib.category.cardio import CardioData
from bushidolib.category.base.unit import Unit

from ..models import CardioUnitTable
from ._base import BaseUnitRepo


class CardioUnitRepo(BaseUnitRepo[CardioData, CardioUnitTable]):
    orm_cls = CardioUnitTable
    data_cls = CardioData

    @override
    def _to_orm(self, unit: Unit) -> CardioUnitTable:
        return CardioUnitTable(
            name=unit.name,
            log_time=unit.log_time,
            start_t=unit.data.start_t,
            seconds=unit.data.seconds,
            gym=unit.data.gym,
            distance=unit.data.distance,
            avg_hr=unit.data.avg_hr,
            max_hr=unit.data.max_hr,
            calories=unit.data.calories,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: CardioUnitTable) -> Unit:
        return Unit(
            name=orm_unit.name,
            data=CardioData(
                start_t=orm_unit.start_t,
                seconds=orm_unit.seconds,
                gym=orm_unit.gym,
                distance=orm_unit.distance,
                avg_hr=orm_unit.avg_hr,
                max_hr=orm_unit.max_hr,
                calories=orm_unit.calories,
            ),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
