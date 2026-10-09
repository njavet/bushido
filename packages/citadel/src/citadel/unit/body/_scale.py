from typing import Literal

from citadel.unit.base import BaseUnit, UnitType


class ScaleUnit(BaseUnit):
    unit_type: Literal[UnitType.scale] = UnitType.scale
