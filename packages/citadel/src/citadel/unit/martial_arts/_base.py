from typing import Literal

from citadel.unit.base import BaseUnit, SpaceTimeData, UnitType


class MartialArtsUnit(BaseUnit, SpaceTimeData):
    unit_type: Literal[UnitType.martial_arts] = UnitType.martial_arts
