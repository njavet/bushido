import datetime
from typing import Literal

from pydantic import BaseModel

from citadel.domain.base import BaseUnit, RawUnit, SpaceTimeData, UnitType
from citadel.domain.parsing import parse_start_end_time_string
from citadel.exceptions import UnitParsingError

# TODO barbell, dumbbell


class LiftingSetData(BaseModel):
    set_nr: int
    rest: float
    weight: float
    reps: float


class LiftingUnit(BaseUnit):
    unit_type: Literal[UnitType.strength] = UnitType.strength
    name: str
    variant: str = "default"
    sets: list[LiftingSetData]


class StrengthUnit(BaseUnit, SpaceTimeData):
    pass


def parse_lifting_data(tokens: tuple[str, ...]) -> list[LiftingSetData]:
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
        LiftingSetData(set_nr=i, weight=weight, reps=rep, rest=rest)
        for i, (weight, rep, rest) in enumerate(zip(weights, reps, rests, strict=False))
    ]


def build_lifting_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> LiftingUnit:
    sets = parse_lifting_data(raw_unit.tokens)
    return LiftingUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        sets=sets,
        variant=raw_unit.options.get("variant", "default"),
    )


def build_strength_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> StrengthUnit:
    start_t, end_t = parse_start_end_time_string(raw_unit.tokens[0])
    try:
        gym = raw_unit.tokens[1]
    except IndexError as e:
        raise UnitParsingError("no gym") from e
    return StrengthUnit(
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=start_t,
        end_t=end_t,
        gym=gym,
    )
