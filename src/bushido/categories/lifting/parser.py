from dataclasses import dataclass

from ..exceptions import ParsingError
from .domain import LiftingSpec, LiftingUnitName, SetSpec


@dataclass(frozen=True, slots=True)
class LiftingParser:
    grammar = """
    <name> (<weight> <reps> [<rest>])+ # [<comment>]
    """
    unit_names = [unit_name.value for unit_name in LiftingUnitName]

    @staticmethod
    def parse(tokens: tuple[str, ...]) -> LiftingSpec:
        try:
            weights = [float(w) for w in tokens[::3]]
        except ValueError:
            raise ParsingError("invalid weight")
        try:
            reps = [float(r) for r in tokens[1::3]]
        except ValueError:
            raise ParsingError("invalid reps")
        try:
            rests = [float(r) for r in tokens[2::3]] + [0]
        except ValueError:
            raise ParsingError("invalid rest")
        if len(weights) == 0:
            raise ParsingError("at least one set")
        if len(weights) != len(reps):
            raise ParsingError("weights and reps don't match")
        if any(x < 0 for x in reps):
            raise ParsingError("reps must all be positive")
        if any(x < 0 for x in weights):
            raise ParsingError("weights must all be positive")
        if any(x < 0 for x in rests):
            raise ParsingError("rests must all be positive")

        return LiftingSpec(
            sets=[
                SetSpec(set_nr=i, weight=weight, reps=rep, rest=rest)
                for i, (weight, rep, rest) in enumerate(zip(weights, reps, rests))
            ]
        )
