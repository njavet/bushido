from bushido.modules.dtypes import Err, Ok, ParsedUnit, Result
from bushido.modules.lifting.domain import LiftingSpec, SetSpec
from bushido.modules.parser import UnitParser


class LiftingParser(UnitParser[LiftingSpec]):
    def _parse_unit(self) -> Result[ParsedUnit[LiftingSpec]]:
        weights = [float(w) for w in self.tokens[::3]]
        reps = [float(r) for r in self.tokens[1::3]]
        rests = [float(r) for r in self.tokens[2::3]] + [0]
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

        pu = ParsedUnit(
            name=self.unit_name,
            data=data,
            comment=self.comment,
            payload=self.payload,
            log_dt=self.log_dt,
        )
        return Ok(pu)
