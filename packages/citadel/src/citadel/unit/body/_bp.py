from typing import Literal

from citadel.unit.base import BaseUnit, UnitType


class BloodPressureUnit(BaseUnit):
    unit_type: Literal[UnitType.blood_pressure] = UnitType.blood_pressure
    systolic: int
    diastolic: int
    heart_rate: int | None = None
