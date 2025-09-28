from bushido.domain.lifting import ExerciseSpec, SetSpec
from bushido.domain.unit import ParsedUnit
from bushido.infra.db import LiftingSet, LiftingUnit


class LiftingMapper:
    def to_orm(
        self, parsed_unit: ParsedUnit[ExerciseSpec]
    ) -> tuple[LiftingUnit, list[LiftingSet]]:
        unit = LiftingUnit(name=parsed_unit.name, comment=parsed_unit.comment)
        lst = []
        for s in parsed_unit.data.sets:
            ls = LiftingSet(weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(ls)
        return unit, lst

    def from_orm(
        self, orms: tuple[LiftingUnit, list[LiftingSet]]
    ) -> ParsedUnit[ExerciseSpec]:
        unit, sets = orms
        lst = []
        for i, s in enumerate(sets):
            sp = SetSpec(set_nr=i, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = ParsedUnit(
            name=unit.name,
            data=ExerciseSpec(sets=lst),
            comment=unit.comment,
        )
        return pu
