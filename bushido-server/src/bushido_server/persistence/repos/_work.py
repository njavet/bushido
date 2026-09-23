from typing import override

from bushidolib.unit.work import WorkUnit

from ..models import WorkUnitTable
from ._base import BaseUnitRepo


class WorkUnitRepo(BaseUnitRepo[WorkUnit, WorkUnitTable]):
    orm_cls = WorkUnitTable

    @override
    def _to_orm(self, unit: WorkUnit) -> WorkUnitTable:
        return WorkUnitTable(
            start_t=unit.start_t,
            end_t=unit.end_t,
            seconds=unit.seconds,
            gym=unit.gym,
            project=unit.project,
            topic=unit.topic,
            log_time=unit.log_time,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: WorkUnitTable) -> WorkUnit:
        return WorkUnit(
            start_t=orm_unit.start_t,
            end_t=orm_unit.end_t,
            seconds=orm_unit.seconds,
            gym=orm_unit.gym,
            project=orm_unit.project,
            topic=orm_unit.topic,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
