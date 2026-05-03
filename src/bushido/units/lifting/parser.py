from bushido.core.result import Err, Ok, Result
from bushido.units.lifting.domain import LiftingSpec, SetSpec
from bushido.units.parsing.base import UnitParser


class LiftingParser(UnitParser[LiftingSpec]):
    grammar = ""

    @staticmethod
    def parse(tokens: tuple[str, ...]) -> Result[LiftingSpec]:
        weights = [float(w) for w in tokens[::3]]
        reps = [float(r) for r in tokens[1::3]]
        rests = [float(r) for r in tokens[2::3]] + [0]
        if len(weights) == 0:
            return Err("at least one set")
        if len(weights) != len(reps):
            return Err("weights and reps must have same length")
        if any(x < 0 for x in reps):
            return Err("reps must all be positive")
        if any(x < 0 for x in weights):
            return Err("weights must all be positive")
        if any(x < 0 for x in rests):
            return Err("rests must all be positive")

        data = LiftingSpec(
            sets=[
                SetSpec(set_nr=i, weight=weight, reps=rep, rest=rest)
                for i, (weight, rep, rest) in enumerate(zip(weights, reps, rests))
            ]
        )
        return Ok(data)
