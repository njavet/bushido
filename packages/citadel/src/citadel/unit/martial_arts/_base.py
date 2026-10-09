import datetime
from typing import Literal

from citadel.exceptions import UnitParsingError
from citadel.unit.base import BaseUnit, RawUnit, SpaceTimeData, UnitType
from citadel.unit.parsing import parse_start_end_time_string


class MartialArtsUnit(BaseUnit, SpaceTimeData):
    unit_type: Literal[UnitType.martial_arts] = UnitType.martial_arts
