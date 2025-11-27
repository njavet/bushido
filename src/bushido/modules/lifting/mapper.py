from bushido.core.dtypes import ParsedUnit, UnitMapper

from .domain import LiftingSpec, SetSpec
from .orm import LiftingSet, LiftingUnit


class LiftingMapper(UnitMapper[LiftingSpec, LiftingUnit, LiftingSet]):
    @staticmethod
    def to_orm(
        parsed_unit: ParsedUnit[LiftingSpec],
    ) -> tuple[LiftingUnit, list[LiftingSet]]:
        unit = LiftingUnit(
            name=parsed_unit.name,
            comment=parsed_unit.comment,
            log_time=parsed_unit.log_time,
        )
        lst = []
        for s in parsed_unit.data.sets:
            ls = LiftingSet(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(ls)
        return unit, lst

    @staticmethod
    def from_orm(orms: tuple[LiftingUnit, list[LiftingSet]]) -> ParsedUnit[LiftingSpec]:
        unit, sets = orms
        lst = []
        for s in sets:
            sp = SetSpec(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = ParsedUnit(
            name=unit.name,
            data=LiftingSpec(sets=lst),
            log_time=unit.log_time,
            comment=unit.comment,
        )
        return pu
