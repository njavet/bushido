from typing import Literal

from pydantic import BaseModel

from citadel.unit import UnitType


class TapeUnit(BaseModel):
    unit_type: Literal[UnitType.tape] = UnitType.tape

    waist: float
    right_arm: float | None = None
    left_arm: float | None = None
    right_leg: float | None = None
    left_leg: float | None = None
    shoulders: float | None = None
    chest: float | None = None
