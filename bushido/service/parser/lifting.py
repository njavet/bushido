# project imports
from bushido.core.result import Ok, Result
from bushido.domain.base import ParsedUnit, UnitSpec
from bushido.domain.lifting import ExerciseSpec, SetSpec
from bushido.service.parser.base import UnitParser


class LiftingParser(UnitParser[ExerciseSpec]):
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit[ExerciseSpec]]:
        weights = [float(w) for w in unit_spec.words[::3]]
        reps = [float(r) for r in unit_spec.words[1::3]]
        rests = [float(r) for r in unit_spec.words[2::3]] + [0]

        ex = ExerciseSpec(
            sets=[
                SetSpec(weight=weight, reps=rep, rest=rest)
                for weight, rep, rest in zip(weights, reps, rests)
            ]
        )

        pu = ParsedUnit(
            unit_name=unit_spec.unit_name,
            data=ex,
            comment=unit_spec.comment,
        )
        return Ok(pu)
