from typing import Literal

from pydantic import BaseModel, Field

from citadel.unit.base import BaseUnit, UnitType


class BilateralSet(BaseModel):
    set_nr: int = Field(ge=0, le=32)
    rest: float = Field(gt=0, le=1024)
    weight: float = Field(ge=0, le=512)
    reps: float = Field(gt=0, le=128)


class BilateralUnit(BaseUnit):
    unit_type: Literal[UnitType.bilateral] = UnitType.bilateral
    name: str
    variant: str = "barbell"
    sets: list[BilateralSet]


class UnilateralSet(BaseModel):
    set_nr: int = Field(ge=0, le=32)
    rest: float = Field(gt=0, le=1024)
    weight_left: float = Field(ge=0, le=512)
    weight_right: float = Field(ge=0, le=512)
    reps_left: float = Field(ge=0, le=128)
    reps_right: float = Field(ge=0, le=128)


class UnilateralUnit(BaseUnit):
    unit_type: Literal[UnitType.unilateral] = UnitType.unilateral
    name: str
    variant: str = "dumbbell"
    sets: list[UnilateralSet]


def parse_bilateral_set_data(tokens: tuple[str, ...]) -> list[BilateralSet]:
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


def parse_unilateral_set_data(tokens: tuple[str, ...]) -> list[BilateralSet]:
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
