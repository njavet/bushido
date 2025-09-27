from bushido.core.result import Err, Ok, Result
from bushido.domain.lifting import ExerciseSpec, SetSpec
from bushido.domain.unit import ParsedUnit, UnitSpec
from bushido.iface.parser.base import UnitParser


class LiftingParser(UnitParser[ExerciseSpec]):
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit[ExerciseSpec]]:
        weights = [float(w) for w in unit_spec.words[::3]]
        reps = [float(r) for r in unit_spec.words[1::3]]
        rests = [float(r) for r in unit_spec.words[2::3]] + [0]
        if len(weights) == 0:
            return Err('at least one set')
        if len(weights) != len(reps):
            return Err('weights and reps must have same length')

        ex = ExerciseSpec(
            sets=[
                SetSpec(weight=weight, reps=rep, rest=rest)
                for weight, rep, rest in zip(weights, reps, rests)
            ]
        )

        pu = ParsedUnit(
            name=unit_spec.name,
            data=ex,
            comment=unit_spec.comment,
        )
        return Ok(pu)
