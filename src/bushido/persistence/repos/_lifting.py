from sqlalchemy.orm import selectinload

from bushido.domain.units import Unit
from bushido.domain.units.lifting import LiftingData, SetData

from ..models import LiftingSet, LiftingUnitTable
from ._base import BaseUnitRepo


class LiftingUnitRepo(BaseUnitRepo[LiftingData, LiftingUnitTable]):
    orm_cls = LiftingUnitTable
    load_options = (selectinload(LiftingUnitTable.subunits),)

    @staticmethod
    def _to_orm(unit: Unit[LiftingData]) -> LiftingUnitTable:
        orm_unit = LiftingUnitTable(
            name=unit.name,
            emoji=unit.emoji,
            comment=unit.comment,
            log_time=unit.log_time,
        )
        orm_unit.subunits = [
            LiftingSet(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            for s in unit.data.sets
        ]
        return orm_unit

    @staticmethod
    def _from_orm(orm_unit: LiftingUnitTable) -> Unit[LiftingData]:
        lst = []
        for s in orm_unit.subunits:
            sp = SetData(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=LiftingData(sets=lst, program=None, variant=None),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
