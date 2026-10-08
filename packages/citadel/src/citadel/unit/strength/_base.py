from typing import Literal

from pydantic import BaseModel, Field

from citadel.unit.base import BaseUnit, UnitType


class SetData(BaseModel):
    set_nr: int = Field(ge=0, le=32)
    rest: float = Field(ge=0, le=1024)
    weight: float = Field(ge=0, le=512)
    reps: float = Field(ge=0, le=128)


class BarbellUnit(BaseUnit):
    unit_type: Literal[UnitType.barbell] = UnitType.barbell
    name: str
    variant: str = "default"
    sets: list[SetData]


class DumbbellUnit(BaseUnit):
    unit_type: Literal[UnitType.dumbbell] = UnitType.dumbbell
    name: str
    variant: str = "default"
    sets_left: list[SetData]
    sets_right: list[SetData]
