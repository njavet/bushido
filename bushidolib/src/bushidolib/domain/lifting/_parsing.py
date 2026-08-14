from bushidolib.exceptions import ParsingUnitError

from ._spec import Data, SetData


def parse(tokens: tuple[str, ...]) -> Data:
    try:
        weights = [float(w) for w in tokens[::3]]
    except ValueError as e:
        raise ParsingUnitError(f"invalid weight {tokens[::3]}") from e
    try:
        reps = [float(r) for r in tokens[1::3]]
    except ValueError as e:
        raise ParsingUnitError(f"invalid reps {tokens[1::3]}") from e
    try:
        rests = [float(r) for r in tokens[2::3]] + [0]
    except ValueError as e:
        raise ParsingUnitError(f"invalid rest {tokens[2::3]}") from e
    if len(weights) == 0:
        raise ParsingUnitError("at least one set")
    if len(weights) != len(reps):
        raise ParsingUnitError("weights and reps don't match")
    if any(x <= 0 for x in reps):
        raise ParsingUnitError("reps must all be positive")
    if any(x <= 0 for x in weights):
        raise ParsingUnitError("weights must all be positive")
    if any(x <= 0 for x in rests[:-1]):
        raise ParsingUnitError("rests must all be positive")

    return Data(
        variant=None,
        program=None,
        sets=[
            SetData(set_nr=i, weight=weight, reps=rep, rest=rest)
            for i, (weight, rep, rest) in enumerate(
                zip(weights, reps, rests, strict=False)
            )
        ],
    )
