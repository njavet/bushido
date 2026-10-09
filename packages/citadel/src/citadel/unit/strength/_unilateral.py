import datetime
from typing import Literal

from pydantic import BaseModel, Field

from citadel.exceptions import UnitParsingError
from citadel.unit.base import BaseUnit, RawUnit, UnitType


class UnilateralSet(BaseModel):
    set_nr: int = Field(ge=0, le=32)
    rest: int = Field(gt=0, le=1024)
    weight_left: float = Field(ge=0, le=512)
    weight_right: float = Field(ge=0, le=512)
    reps_left: float = Field(ge=0, le=128)
    reps_right: float = Field(ge=0, le=128)


class UnilateralUnit(BaseUnit):
    unit_type: Literal[UnitType.unilateral] = UnitType.unilateral
    name: str
    variant: str = "dumbbell"
    sets: list[UnilateralSet] = Field(min_length=1)


def parse_unilateral_set_data(tokens: tuple[str, ...]) -> list[UnilateralSet]:
    i = 0
    set_nr = 0
    sets = []
    while i + 2 < len(tokens):
        try:
            weight_left, weight_right = tokens[i + 1].split(",")
            reps_left, reps_right = tokens[i + 2].split(",")
            s = UnilateralSet(
                set_nr=set_nr,
                rest=int(tokens[i]),
                weight_left=float(weight_left),
                weight_right=float(weight_right),
                reps_left=float(reps_left),
                reps_right=float(reps_right),
            )
        except Exception as e:
            raise UnitParsingError(f"invalid set {tokens[i : i + 3]}") from e
        else:
            sets.append(s)
            i += 3
            set_nr += 1
    return sets
