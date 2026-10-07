from typing import override

from citadel.domain.unit import ChronoUnit, UnitType

from ..models import ChronoUnitTable, UnitTable
from ._base import BaseUnitRepo


class ChronoUnitRepo(BaseUnitRepo[ChronoUnit]):
    unit_type = UnitType.chrono

    @override
    def add_unit(self, unit: ChronoUnit, spartan_id: int) -> None:
        orm_unit = UnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            chrono=ChronoUnitTable(
                seconds=unit.seconds,
            ),
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: UnitTable) -> ChronoUnit:
        assert orm_unit.chrono is not None
        return ChronoUnit(
            name=orm_unit.name,
            seconds=orm_unit.chrono.seconds,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
