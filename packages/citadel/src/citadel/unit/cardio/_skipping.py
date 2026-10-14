import datetime
from typing import Literal

from citadel.bcl import LogUnitCommand
from citadel.unit.base import BaseUnit, UnitType

from ._base import CardioData, parse_cardio_data


class SkippingUnit(BaseUnit, CardioData):
    unit_type: Literal[UnitType.skipping] = UnitType.skipping


def build_skipping_unit(raw_unit: LogUnitCommand, log_time: datetime.datetime) -> SkippingUnit:
    data = parse_cardio_data(raw_unit.args, raw_unit.options)
    return SkippingUnit(
        name=raw_unit.unit_name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=data.start_t,
        seconds=data.seconds,
        gym=data.gym,
        avg_hr=data.avg_hr,
        max_hr=data.max_hr,
        calories=data.calories,
    )
