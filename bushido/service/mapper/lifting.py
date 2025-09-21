# project imports
from bushido.domain.base import ParsedUnit
from bushido.db import Exercise, LiftingSet
from bushido.domain.lifting import ExerciseSpec, SetSpec
from bushido.service.mapper.base import UnitMapper


class LiftingMapper(UnitMapper[ExerciseSpec, Exercise, LiftingSet]):
    def to_orm(self, parsed_unit: ParsedUnit[ExerciseSpec]
    ) -> tuple[Exercise, list[LiftingSet]]:
        unit = Exercise(name=parsed_unit.unit_name,
                        comment=parsed_unit.comment)
        lst = []
        for s in parsed_unit.data.sets:
            ls = LiftingSet(weight=s.weight,
                            reps=s.reps,
                            rest=s.rest)
            lst.append(ls)
        return unit, lst

    def from_orm(self, orms: tuple[Exercise, list[LiftingSet]]) -> ParsedUnit[ExerciseSpec]:
        unit, sets = orms
        lst = []
        for s in sets:
            sp = SetSpec(weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = ParsedUnit(unit_name=unit.name,
                        data=ExerciseSpec(sets=lst),
                        comment=unit.comment)
        return pu
