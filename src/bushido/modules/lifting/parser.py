from bushido.modules.domain import Err, Ok, ParsedUnit, Result
from bushido.modules.lifting.domain import LiftingUnitName, SetSpec
from bushido.modules.parser import UnitParser


class LiftingParser(UnitParser[list[SetSpec]]):
    def _parse_unit_name(self, tokens: list[str]) -> Result[list[str]]:
        if len(tokens) == 0:
            return Err("no unit name")
        if tokens[0] not in [u.name for u in LiftingUnitName]:
            return Err("invalid unit name")
        self.unit_name = tokens[0]
        return Ok(tokens[1:])

    def _parse_unit(self) -> Result[ParsedUnit[list[SetSpec]]]:
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

        sets = [
            SetSpec(set_nr=i, weight=weight, reps=rep, rest=rest)
            for i, (weight, rep, rest) in enumerate(zip(weights, reps, rests))
        ]

        pu = ParsedUnit(
            name=self.unit_name,
            data=sets,
            comment=self.comment,
            log_dt=self.log_dt,
        )
        return Ok(pu)
