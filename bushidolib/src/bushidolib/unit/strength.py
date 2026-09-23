import datetime

from pydantic import BaseModel

from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import parse_space_time_data
from bushidolib.unit.base import BaseUnit, RawUnit, SpaceTimeData


class LiftingSetData(BaseModel):
    set_nr: int
    rest: float
    weight: float
    reps: float


class LiftingData(BaseModel):
    sets: list[LiftingSetData]


class LiftingUnit(BaseUnit, LiftingData):
    exercise: str
    variant: str = "default"


class StrengthUnit(BaseUnit, SpaceTimeData):
    pass


def parse_lifting_data(tokens: tuple[str, ...]) -> LiftingData:
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

    return LiftingData(
        sets=[
            LiftingSetData(set_nr=i, weight=weight, reps=rep, rest=rest)
            for i, (weight, rep, rest) in enumerate(
                zip(weights, reps, rests, strict=False)
            )
        ],
    )


def build_lifting_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> LiftingUnit:
    data = parse_lifting_data(raw_unit.tokens)
    return LiftingUnit(
        exercise=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        sets=data.sets,
        variant=raw_unit.options.get('variant', 'default')
    )


def build_strength_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> StrengthUnit:
    data = parse_space_time_data(raw_unit.tokens)
    return StrengthUnit(
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=data.start_t,
        end_t=data.end_t,
        gym=data.gym,
    )
