from .domain import LiftingSpec, LiftingUnit, SetSpec
from .db_model import LiftingSet, LiftingUnitTable


class LiftingMapper:
    @staticmethod
    def to_orm(parsed_unit: LiftingUnit) -> LiftingUnitTable:
        unit = LiftingUnitTable(
            name=parsed_unit.name,
            emoji=parsed_unit.emoji,
            comment=parsed_unit.comment,
            log_time=parsed_unit.log_time,
        )
        unit.subunits = [
            LiftingSet(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            for s in parsed_unit.data.sets
        ]
        return unit

    @staticmethod
    def from_orm(orm_unit: LiftingUnitTable) -> LiftingUnit:
        lst = []
        for s in orm_unit.subunits:
            sp = SetSpec(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = LiftingUnit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=LiftingSpec(sets=lst),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
