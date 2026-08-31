from typing import override

from sqlalchemy.orm import selectinload

from bushidolib.lifting import LiftingData, LiftingSetData, LiftingUnit

from ..models import LiftingSet, LiftingUnitTable
from ._base import BaseUnitRepo


class LiftingUnitRepo(BaseUnitRepo[LiftingUnit, LiftingUnitTable]):
    orm_cls = LiftingUnitTable
    load_options = (selectinload(LiftingUnitTable.subunits),)

    @override
    def _to_orm(self, unit: LiftingUnit) -> LiftingUnitTable:
        setting_id = self.get_unit_config_id(unit.name)
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
    def _from_orm(self, orm_unit: LiftingUnitTable) -> LiftingUnit:
        name = self.get_unit_setting_name(orm_unit.unit_setting_id)
        lst = []
        for s in orm_unit.subunits:
            sp = LiftingSetData(
                set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest
            )
            lst.append(sp)
        return LiftingUnit(
            name=name,
            data=LiftingData(sets=lst, program=None, variant=None),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
