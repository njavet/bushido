import datetime
from typing import Literal

from pydantic import BaseModel

from citadel.exceptions import UnitParsingError
from citadel.unit.base import BaseUnit, RawUnit, UnitType
from citadel.unit.parsing import (
    parse_military_time_string,
    time_string_to_seconds,
)

from ._base import CardioData, parse_cardio_data


class SkippingUnit(BaseUnit, CardioData):
    unit_type: Literal[UnitType.skipping] = UnitType.skipping


def build_skipping_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> SkippingUnit:
    data = parse_cardio_data(raw_unit.tokens, raw_unit.options)
    return SkippingUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=data.start_t,
        seconds=data.seconds,
        gym=data.gym,
        avg_hr=data.avg_hr,
        max_hr=data.max_hr,
        calories=data.calories,
    )
