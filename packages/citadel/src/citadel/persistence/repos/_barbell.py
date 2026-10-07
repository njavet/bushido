from typing import override

from sqlalchemy.orm import selectinload

from citadel.domain.unit import BarbellUnit, SetData, UnitType

from ..models import BarbellSet, BarbellUnitTable, UnitTable
from ._base import BaseUnitRepo


class BarbellUnitRepo(BaseUnitRepo[BarbellUnit, BarbellUnitTable]):
    orm_cls = BarbellUnitTable
    unit_type = UnitType.barbell
    load_options = (selectinload(BarbellUnitTable.subunits),)

    @override
    def add_unit(self, unit: BarbellUnit, spartan_id: int) -> None:
        orm_unit = BarbellUnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            variant=unit.variant,
            subunits=[
                BarbellSet(
                    set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest
                )
                for s in unit.sets
            ],
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: BarbellUnitTable) -> BarbellUnit:
        sets = [
            SetData(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            for s in orm_unit.subunits
        ]
        return BarbellUnit(
            name=orm_unit.name,
            variant=orm_unit.variant,
            sets=sets,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
