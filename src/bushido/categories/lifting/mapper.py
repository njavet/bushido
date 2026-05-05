from ..dtypes import ParsedUnit
from .orm import LiftingSet, LiftingUnitTable
from .parser import LiftingSpec, SetSpec


class LiftingMapper:
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[LiftingSpec]) -> LiftingUnitTable:
        unit = LiftingUnitTable(
            name=parsed_unit.name,
            comment=parsed_unit.comment,
            log_time=parsed_unit.log_time,
        )
        unit.subunits = [
            LiftingSet(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            for s in parsed_unit.data.sets
        ]
        return unit

    @staticmethod
    def from_orm(orm_unit: LiftingUnitTable) -> ParsedUnit[LiftingSpec]:
        lst = []
        for s in orm_unit.subunits:
            sp = SetSpec(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = ParsedUnit(
            name=orm_unit.name,
            data=LiftingSpec(sets=lst),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
