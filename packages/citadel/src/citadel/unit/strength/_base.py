from typing import Literal

from pydantic import BaseModel, Field

from citadel.unit.base import BaseUnit, UnitType


class BilateralSet(BaseModel):
    set_nr: int = Field(ge=0, le=32)
    rest: float = Field(ge=0, le=1024)
    weight: float = Field(ge=0, le=512)
    reps: float = Field(ge=0, le=128)


class BilateralUnit(BaseUnit):
    unit_type: Literal[UnitType.bilateral] = UnitType.bilateral
    name: str
    variant: str = "default"
    sets: list[BilateralSet]


class DumbbellSet(BaseModel):
    set_nr: int = Field(ge=0, le=32)
    rest: float = Field(ge=0, le=1024)
    weight_left: float = Field(ge=0, le=512)
    weight_right: float = Field(ge=0, le=512)
    reps_left: float = Field(ge=0, le=128)
    reps_right: float = Field(ge=0, le=128)


class DumbbellUnit(BaseUnit):
    unit_type: Literal[UnitType.unilateral] = UnitType.unilateral
    name: str
    variant: str = "default"
    sets: list[DumbbellSet]
