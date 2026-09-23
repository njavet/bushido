from typing import override

from bushidolib.unit.log import LogUnit

from ..models import LogUnitTable
from ._base import BaseUnitRepo


class LogUnitRepo(BaseUnitRepo[LogUnit, LogUnitTable]):
    orm_cls = LogUnitTable

    @override
    def _to_orm(self, unit: LogUnit) -> LogUnitTable:
        return LogUnitTable(
            name=unit.name,
            kind=unit.kind,
            log_time=unit.log_time,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: LogUnitTable) -> LogUnit:
        return LogUnit(
            name=orm_unit.name,
            kind=orm_unit.kind,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
