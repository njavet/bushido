from typing import Literal

from citadel.unit.base import BaseUnit, UnitType


class ScaleUnit(BaseUnit):
    unit_type: Literal[UnitType.scale] = UnitType.scale

    weight: float
    fat: float | None = None
    muscle: float | None = None
    water: float | None = None
    pwv: float | None = None  # m/s
    visceral_fat_index: float | None = None
    lean_right_arm: float | None = None
    lean_left_arm: float | None = None
    lean_right_leg: float | None = None
    lean_left_leg: float | None = None
    lean_torso: float | None = None
    fat_right_arm: float | None = None
    fat_left_arm: float | None = None
    fat_right_leg: float | None = None
    fat_left_leg: float | None = None
    fat_torso: float | None = None
