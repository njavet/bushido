import datetime

from bushidolib.exceptions import UnitParsingError

from ..base import RawUnit
from ._spec import LiftingData, LiftingSetData, LiftingUnit


def parse_lifting_data(tokens: tuple[str, ...]) -> LiftingData:
    try:
        weights = [float(w) for w in tokens[::3]]
    except ValueError as e:
        raise UnitParsingError(f"invalid weight {tokens[::3]}") from e
    try:
        reps = [float(r) for r in tokens[1::3]]
    except ValueError as e:
        raise UnitParsingError(f"invalid reps {tokens[1::3]}") from e
    try:
        rests = [float(r) for r in tokens[2::3]] + [0]
    except ValueError as e:
        raise UnitParsingError(f"invalid rest {tokens[2::3]}") from e
    if len(weights) == 0:
        raise UnitParsingError("at least one set")
    if len(weights) != len(reps):
        raise UnitParsingError("weights and reps don't match")
    if any(x <= 0 for x in reps):
        raise UnitParsingError("reps must all be positive")
    if any(x <= 0 for x in weights):
        raise UnitParsingError("weights must all be positive")
    if any(x <= 0 for x in rests[:-1]):
        raise UnitParsingError("rests must all be positive")

    return LiftingData(
        variant=None,
        sets=[
            LiftingSetData(set_nr=i, weight=weight, reps=rep, rest=rest)
            for i, (weight, rep, rest) in enumerate(
                zip(weights, reps, rests, strict=False)
            )
        ],
    )


def build_lifting_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> LiftingUnit:
    lifting_data = parse_lifting_data(raw_unit.tokens)
    return LiftingUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        sets=lifting_data.sets,
        variant=lifting_data.variant,
    )
