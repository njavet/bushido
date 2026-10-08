import datetime

from citadel.exceptions import UnitParsingError
from citadel.unit.base import RawUnit

from ._base import BilateralSet


def parse_barbell_set_data(tokens: tuple[str, ...]) -> list[BilateralSet]:
    try:
        rests = [float(r) for r in tokens[::3]]
    except ValueError as e:
        raise UnitParsingError(f"invalid rest {tokens[::3]}") from e
    try:
        weights = [float(w) for w in tokens[1::3]]
    except ValueError as e:
        raise UnitParsingError(f"invalid weight {tokens[1::3]}") from e
    try:
        reps = [float(r) for r in tokens[2::3]]
    except ValueError as e:
        raise UnitParsingError(f"invalid reps {tokens[2::3]}") from e
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

    return [
        BilateralSet(set_nr=i, weight=weight, reps=rep, rest=rest)
        for i, (weight, rep, rest) in enumerate(zip(weights, reps, rests, strict=False))
    ]


def build_barbell_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> BarbellUnit:
    sets = parse_set_data(raw_unit.tokens)
    return BarbellUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        sets=sets,
        variant=raw_unit.options.get("variant", "default"),
    )
