from bushido.unit.base import Unit

from .db_model import BarbellSet, BarbellUnitTable
from .unit import BarbellData, SetData


class BarbellMapper:
    @staticmethod
    def to_orm(unit: Unit[BarbellData]) -> BarbellUnitTable:
        orm_unit = BarbellUnitTable(
            name=unit.name,
            emoji=unit.emoji,
            comment=unit.comment,
            log_time=unit.log_time,
        )
        orm_unit.sets = [
            BarbellSet(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            for s in unit.data.sets
        ]
        return orm_unit

    @staticmethod
    def from_orm(orm_unit: BarbellUnitTable) -> Unit[BarbellData]:
        lst = []
        for s in orm_unit.sets:
            sp = SetData(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=BarbellData(sets=lst, program=None, variant=None),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
