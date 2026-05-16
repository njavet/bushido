from dataclasses import dataclass

from bushido.units.exceptions import ParsingError

from .unit import Data, SetData


@dataclass(frozen=True, slots=True)
class Parser:
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> Data:
        try:
            weights = [float(w) for w in tokens[::3]]
        except ValueError:
            raise ParsingError(f"invalid weight {tokens[::3]}")
        try:
            reps = [float(r) for r in tokens[1::3]]
        except ValueError:
            raise ParsingError(f"invalid reps {tokens[1::3]}")
        try:
            rests = [float(r) for r in tokens[2::3]] + [0]
        except ValueError:
            raise ParsingError(f"invalid rest {tokens[2::3]}")
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

        return Data(
            variant=None,
            program=None,
            sets=[
                SetData(set_nr=i, weight=weight, reps=rep, rest=rest)
                for i, (weight, rep, rest) in enumerate(zip(weights, reps, rests))
            ],
        )
