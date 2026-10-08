import datetime
from typing import Literal

from pydantic import BaseModel, Field

from citadel.exceptions import UnitParsingError
from citadel.unit.base import BaseUnit, RawUnit, UnitType


class BilateralSet(BaseModel):
    set_nr: int = Field(ge=0, le=32)
    rest: int = Field(gt=0, le=1024)
    weight: float = Field(ge=0, le=512)
    reps: float = Field(gt=0, le=128)


class BilateralUnit(BaseUnit):
    unit_type: Literal[UnitType.bilateral] = UnitType.bilateral
    name: str
    variant: str = "barbell"
    sets: list[BilateralSet] = Field(min_length=1)


def parse_bilateral_set_data(tokens: tuple[str, ...]) -> list[BilateralSet]:
    i = 0
    set_nr = 0
    sets = []
    while i + 2 < len(tokens):
        try:
            s = BilateralSet(
                set_nr=set_nr,
                rest=int(tokens[i]),
                weight=float(tokens[i + 1]),
                reps=float(tokens[i + 2]),
            )
        except Exception as e:
            raise UnitParsingError(f"invalid set {tokens[i : i + 3]}") from e
        else:
            sets.append(s)
            i += 3
            set_nr += 1
    return sets


def build_bilateral_unit(
    raw_unit: RawUnit, log_time: datetime.datetime
) -> BilateralUnit:
    sets = parse_bilateral_set_data(raw_unit.tokens)
    return BilateralUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        sets=sets,
        variant=raw_unit.options.get("variant", "default"),
    )
