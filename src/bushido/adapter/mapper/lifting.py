from bushido.db.model import LiftingSet, LiftingUnitTable
from bushido.units.base import Unit
from bushido.units.lifting.unit import Data, SetData


class LiftingMapper:
    @staticmethod
    def to_orm(unit: Unit[Data]) -> LiftingUnitTable:
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
    def from_orm(orm_unit: LiftingUnitTable) -> Unit[Data]:
        lst = []
        for s in orm_unit.subunits:
            sp = SetData(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=Data(sets=lst, program=None, variant=None),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
