from typing import override

from bushidolib.gym import GymData, GymUnit

from ..models import GymUnitTable
from ._base import BaseUnitRepo


class GymUnitRepo(BaseUnitRepo[GymUnit, GymUnitTable]):
    orm_cls = GymUnitTable

    @override
    def _to_orm(self, unit: GymUnit) -> GymUnitTable:
        setting_id = self.get_unit_config_id(unit.name)
        return GymUnitTable(
            unit_setting_id=setting_id,
            log_time=unit.log_time,
            start_t=unit.data.start_t,
            end_t=unit.data.end_t,
            gym=unit.data.gym,
            training=unit.data.training,
            focus=unit.data.focus,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: GymUnitTable) -> GymUnit:
        name = self.get_unit_setting_name(orm_unit.unit_setting_id)
        return GymUnit(
            name=name,
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
