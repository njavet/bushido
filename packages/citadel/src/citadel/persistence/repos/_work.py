from typing import override

from citadel.domain.unit import WorkUnit

from ..models import UnitTable, WorkUnitTable
from ._base import BaseUnitRepo


class WorkUnitRepo(BaseUnitRepo[WorkUnit]):
    orm_cls = WorkUnitTable

    @override
    def add_unit(self, unit: WorkUnit, spartan_id: int) -> None:
        orm_unit = UnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            work=WorkUnitTable(
                start_t=unit.start_t,
                end_t=unit.end_t,
                seconds=unit.seconds,
                gym=unit.gym,
                project=unit.project,
                topic=unit.topic,
            ),
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: UnitTable) -> WorkUnit:
        assert orm_unit.work is not None
        return WorkUnit(
            name=orm_unit.name,
            start_t=orm_unit.work.start_t,
            end_t=orm_unit.work.end_t,
            seconds=orm_unit.work.seconds,
            gym=orm_unit.work.gym,
            project=orm_unit.work.project,
            topic=orm_unit.work.topic,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
