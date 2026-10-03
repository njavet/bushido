from typing import override

from sqlalchemy.orm import selectinload

from citadel.domain.unit.barbell import BarbellUnit, SetData

from ..models import BarbellUnitTable, BarbellSet
from ._base import BaseUnitRepo


class BarbellUnitRepo(BaseUnitRepo[BarbellUnit, BarbellUnitTable]):
    orm_cls = BarbellUnitTable
    load_options = (selectinload(BarbellUnitTable.subunits),)

    @override
    def _to_orm(self, unit: BarbellUnit) -> BarbellUnitTable:
        orm_unit = BarbellUnitTable(
            name=unit.name,
            variant=unit.variant,
            comment=unit.comment,
            log_time=unit.log_time,
        )
        orm_unit.subunits = [
            BarbellSet(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            for s in unit.sets
        ]
        return orm_unit

    @override
    def _from_orm(self, orm_unit: BarbellUnitTable) -> BarbellUnit:
        lst = []
        for s in orm_unit.subunits:
            sp = SetData(
                set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest
            )
            lst.append(sp)
        return BarbellUnit(
            name=orm_unit.name,
            variant=orm_unit.variant,
            sets=lst,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
