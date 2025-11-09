from bushido.infra.db import LiftingSet, LiftingUnit
from bushido.modules.domain import ParsedUnit
from bushido.modules.lifting.domain import SetSpec


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
        sets = []
        for i, s in enumerate(sets):
            sp = SetSpec(set_nr=i, weight=s.weight, reps=s.reps, rest=s.rest)
            sets.append(sp)
        pu = ParsedUnit(
            name=unit.name,
            data=sets,
            comment=unit.comment,
        )
        return pu
