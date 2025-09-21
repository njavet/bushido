# project imports
from bushido.core.result import Ok, Err, Result
from bushido.core.unit import UnitName
from bushido.domain.base import UnitSpec, ParsedUnit
from bushido.domain.lifting import SetSpec, Exercise
from bushido.service.parser.base import UnitParser


class LiftingParser(UnitParser):
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit]:
        weights = [float(w) for w in unit_spec.words[::3]]
        reps = [float(r) for r in unit_spec.words[1::3]]
        rests = [float(r) for r in unit_spec.words[2::3]] + [0]

        ex = Exercise(
            sets=[
                SetSpec(weight=weight, reps=rep, rest=rest)
                for weight, rep, rest in zip(weights, reps, rests)
            ]
        )

        pu = ParsedUnit(
            unit_name=UnitName(unit_spec.unit_name),
            data=ex,
            comment=unit_spec.comment,
        )
        return Ok(pu)
