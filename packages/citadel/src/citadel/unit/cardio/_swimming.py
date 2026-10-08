import datetime
from typing import Literal

from citadel.exceptions import UnitParsingError
from citadel.unit.base import BaseUnit, RawUnit, UnitType

from ._base import CardioData, parse_cardio_data


class SwimmingUnit(BaseUnit, CardioData):
    unit_type: Literal[UnitType.swimming] = UnitType.swimming
    distance: float
    pool_length: int | None = None
    temperature: float | None = None


def build_swimming_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> SwimmingUnit:
    data = parse_cardio_data(raw_unit.tokens, raw_unit.options)
    try:
        distance = float(raw_unit.tokens[3])
    except (KeyError, ValueError) as e:
        raise UnitParsingError(f"wrong distance {raw_unit.tokens}") from e
    try:
        pool_length = int(raw_unit.options["pl"])
    except KeyError, ValueError:
        pool_length = None
    try:
        temperature = float(raw_unit.options["tmp"])
    except KeyError, ValueError:
        temperature = None
    return SwimmingUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=data.start_t,
        seconds=data.seconds,
        gym=data.gym,
        distance=distance,
        pool_length=pool_length,
        temperature=temperature,
        avg_hr=data.avg_hr,
        max_hr=data.max_hr,
        calories=data.calories,
    )
