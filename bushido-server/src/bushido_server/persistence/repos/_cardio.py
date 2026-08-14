from typing import override

from bushidolib.domain import Unit
from bushidolib.domain.cardio import CardioData

from ..models import CardioUnitTable
from ._base import BaseUnitRepo


class CardioUnitRepo(BaseUnitRepo[CardioData, CardioUnitTable]):
    orm_cls = CardioUnitTable

    @override
    @staticmethod
    def _to_orm(unit: Unit[CardioData]) -> CardioUnitTable:
        return CardioUnitTable(
            name=unit.name,
            log_time=unit.log_time,
            start_t=unit.data.start_t,
            seconds=unit.data.seconds,
            location=unit.data.location,
            distance=unit.data.distance,
            avg_hr=unit.data.avg_hr,
            max_hr=unit.data.max_hr,
            calories=unit.data.calories,
            comment=unit.comment,
        )

    @override
    @staticmethod
    def _from_orm(orm_unit: CardioUnitTable) -> Unit[CardioData]:
        return Unit(
            name=orm_unit.name,
            data=CardioData(
                start_t=orm_unit.start_t,
                seconds=orm_unit.seconds,
                location=orm_unit.location,
                distance=orm_unit.distance,
                avg_hr=orm_unit.avg_hr,
                max_hr=orm_unit.max_hr,
                calories=orm_unit.calories,
            ),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
