from typing import override

from citadel.domain.unit import LogUnit, UnitType

from ..models import LogUnitTable, UnitTable
from ._base import BaseUnitRepo


class LogUnitRepo(BaseUnitRepo[LogUnit, LogUnitTable]):
    orm_cls = LogUnitTable
    unit_type = UnitType.log

    @override
    def add_unit(self, unit: LogUnit, spartan_id: int) -> None:
        orm_unit = UnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            kind=unit.kind,
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: LogUnitTable) -> LogUnit:
        return LogUnit(
            name=orm_unit.name,
            kind=orm_unit.kind,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
