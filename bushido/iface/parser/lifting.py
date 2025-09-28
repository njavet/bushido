from bushido.core.conf import LiftingUnitName
from bushido.core.result import Err, Ok, Result
from bushido.domain.lifting import ExerciseSpec, SetSpec
from bushido.domain.unit import ParsedUnit, UnitSpec


class LiftingParser:
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit[ExerciseSpec]]:
        if unit_spec.name not in [u.name for u in LiftingUnitName]:
            return Err('invalid unit name')

        weights = [float(w) for w in unit_spec.words[::3]]
        reps = [float(r) for r in unit_spec.words[1::3]]
        rests = [float(r) for r in unit_spec.words[2::3]] + [0]
        if len(weights) == 0:
            return Err('at least one set')
        if len(weights) != len(reps):
            return Err('weights and reps must have same length')
        if any(x < 0 for x in reps):
            return Err('reps must all be positive')
        if any(x < 0 for x in weights):
            return Err('weights must all be positive')
        if any(x < 0 for x in rests):
            return Err('rests must all be positive')

        ex = ExerciseSpec(
            sets=[
                SetSpec(set_nr=i, weight=weight, reps=rep, rest=rest)
                for i, (weight, rep, rest) in enumerate(
                    zip(weights, reps, rests)
                )
            ]
        )

        pu = ParsedUnit(
            name=unit_spec.name,
            data=ex,
            comment=unit_spec.comment,
        )
        return Ok(pu)
