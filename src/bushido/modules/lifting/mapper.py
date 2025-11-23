from bushido.modules.dtypes import ParsedUnit
from bushido.modules.lifting.domain import SetSpec
from bushido.modules.lifting.orm import LiftingSet, LiftingUnit


class LiftingMapper:
    def to_orm(
        self, parsed_unit: ParsedUnit[list[SetSpec]]
    ) -> tuple[LiftingUnit, list[LiftingSet]]:
        unit = LiftingUnit(name=parsed_unit.name, comment=parsed_unit.comment)
        lst = []
        for i, s in enumerate(parsed_unit.data):
            ls = LiftingSet(set_nr=i, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(ls)
        return unit, lst

    def from_orm(
        self, orms: tuple[LiftingUnit, list[LiftingSet]]
    ) -> ParsedUnit[list[SetSpec]]:
        unit, sets = orms
        lst = []
        for i, s in enumerate(sets):
            sp = SetSpec(set_nr=i, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = ParsedUnit(
            name=unit.name,
            data=lst,
            comment=unit.comment,
        )
        return pu
