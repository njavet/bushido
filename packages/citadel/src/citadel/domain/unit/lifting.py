import datetime
from typing import Literal

from citadel.domain.parsing import parse_start_end_time_string
from citadel.exceptions import UnitParsingError

from .base import BaseUnit, RawUnit, SpaceTimeData, UnitType


class LiftingUnit(BaseUnit, SpaceTimeData):
    unit_type: Literal[UnitType.lifting] = UnitType.lifting


def build_lifting_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> LiftingUnit:
    start_t, end_t = parse_start_end_time_string(raw_unit.tokens[0])
    try:
        gym = raw_unit.tokens[1]
    except IndexError as e:
        raise UnitParsingError("no gym") from e
    return LiftingUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=start_t,
        end_t=end_t,
        gym=gym,
    )
