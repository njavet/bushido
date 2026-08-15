from typing import override

from bushidolib.domain import Unit
from bushidolib.cardio import CardioData

from ..models import CardioUnitTable
from ._base import BaseUnitRepo


class CardioUnitRepo(BaseUnitRepo[CardioData, CardioUnitTable]):
    orm_cls = CardioUnitTable

    @override
    def _to_orm(self, unit: Unit[CardioData]) -> CardioUnitTable:
        setting_id = self.get_unit_setting_id(unit.name)
        return CardioUnitTable(
            unit_setting_id=setting_id,
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
    def _from_orm(self, orm_unit: CardioUnitTable) -> Unit[CardioData]:
        name = self.get_unit_setting_name(orm_unit.unit_setting_id)
        return Unit(
            name=name,
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
