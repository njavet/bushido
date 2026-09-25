from typing import override

from bushidolib.unit.cali import CaliUnit

from ..models import CaliUnitTable
from ._base import BaseUnitRepo


class CaliUnitRepo(BaseUnitRepo[CaliUnit, CaliUnitTable]):
    orm_cls = CaliUnitTable

    @override
    def _to_orm(self, unit: CaliUnit) -> CaliUnitTable:
        return CaliUnitTable(
            pushups=unit.pushups,
            squats=unit.squats,
            situps=unit.situps,
            pullups=unit.pullups,
            log_time=unit.log_time,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: CaliUnitTable) -> CaliUnit:
        return CaliUnit(
            pushups=orm_unit.pushups,
            squats=orm_unit.squats,
            situps=orm_unit.situps,
            pullups=orm_unit.pullups,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
