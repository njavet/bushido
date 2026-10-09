from typing import override

from citadel.unit import UnitType
from citadel.unit.work import WorkUnit

from ..models import WorkUnitTable
from ._base import BaseUnitRepo


class WorkUnitRepo(BaseUnitRepo[WorkUnit, WorkUnitTable]):
    orm_cls = WorkUnitTable
    unit_type = UnitType.work

    @override
    def add_unit(self, unit: WorkUnit, spartan_id: int) -> None:
        orm_unit = WorkUnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            start_t=unit.start_t,
            end_t=unit.end_t,
            seconds=unit.seconds,
            gym=unit.gym,
            project=unit.project,
            topic=unit.topic,
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: WorkUnitTable) -> WorkUnit:
        return WorkUnit(
            name=orm_unit.name,
            start_t=orm_unit.start_t,
            end_t=orm_unit.end_t,
            seconds=orm_unit.seconds,
            gym=orm_unit.gym,
            project=orm_unit.project,
            topic=orm_unit.topic,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
