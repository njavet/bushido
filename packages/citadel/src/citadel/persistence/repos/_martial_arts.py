from typing import override

from citadel.domain.unit import MartialArtsUnit, UnitType

from ..models import MartialArtsUnitTable, UnitTable
from ._base import BaseUnitRepo


class MartialArtsUnitRepo(BaseUnitRepo[MartialArtsUnit]):
    unit_type = UnitType.martial_arts

    @override
    def add_unit(self, unit: MartialArtsUnit, spartan_id: int) -> None:
        orm_unit = UnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            martial_arts=MartialArtsUnitTable(
                start_t=unit.start_t,
                end_t=unit.end_t,
                gym=unit.gym,
            ),
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: UnitTable) -> MartialArtsUnit:
        assert orm_unit.martial_arts is not None
        return MartialArtsUnit(
            name=orm_unit.name,
            start_t=orm_unit.martial_arts.start_t,
            end_t=orm_unit.martial_arts.end_t,
            gym=orm_unit.martial_arts.gym,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
