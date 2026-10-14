import datetime
from typing import Literal

from citadel.bcl import LogUnitCommand
from citadel.exceptions import UnitParsingError
from citadel.unit.base import BaseUnit, UnitType

from ._base import CardioData, parse_cardio_data


class RunningUnit(BaseUnit, CardioData):
    unit_type: Literal[UnitType.running] = UnitType.running
    distance: float


def build_running_unit(raw_unit: LogUnitCommand, log_time: datetime.datetime) -> RunningUnit:
    data = parse_cardio_data(raw_unit.args, raw_unit.options)
    try:
        distance = float(raw_unit.args[3])
    except (KeyError, ValueError) as e:
        raise UnitParsingError(f"wrong distance {raw_unit.args}") from e
    return RunningUnit(
        name=raw_unit.unit_name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=data.start_t,
        seconds=data.seconds,
        gym=data.gym,
        distance=distance,
        avg_hr=data.avg_hr,
        max_hr=data.max_hr,
        calories=data.calories,
    )
