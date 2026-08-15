from typing import override

from bushidolib.domain import Unit
from sqlalchemy.orm import selectinload

from bushidolib.lifting import LiftingData, SetData

from ..models import LiftingSet, LiftingUnitTable
from ._base import BaseUnitRepo


class LiftingUnitRepo(BaseUnitRepo[LiftingData, LiftingUnitTable]):
    orm_cls = LiftingUnitTable
    load_options = (selectinload(LiftingUnitTable.subunits),)

    @override
    def _to_orm(self, unit: Unit[LiftingData]) -> LiftingUnitTable:
        setting_id = self.get_unit_setting_id(unit.name)
        orm_unit = LiftingUnitTable(
            unit_setting_id=setting_id,
            comment=unit.comment,
            log_time=unit.log_time,
        )
        orm_unit.subunits = [
            LiftingSet(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            for s in unit.data.sets
        ]
        return orm_unit

    @override
    def _from_orm(self, orm_unit: LiftingUnitTable) -> Unit[LiftingData]:
        name = self.get_unit_setting_name(orm_unit.unit_setting_id)
        lst = []
        for s in orm_unit.subunits:
            sp = SetData(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        return Unit(
            name=name,
            data=LiftingData(sets=lst, program=None, variant=None),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
