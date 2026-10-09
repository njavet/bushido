import datetime
from typing import Literal

from pydantic import BaseModel, Field

from citadel.exceptions import UnitParsingError
from citadel.unit.base import BaseUnit, RawUnit, UnitType
from citadel.unit.strength import BilateralUnit
from citadel.unit.strength._bilateral import parse_bilateral_set_data


def build_squat_unit(
    raw_unit: RawUnit, log_time: datetime.datetime
) -> BilateralUnit:
    sets = parse_bilateral_set_data(raw_unit.tokens)
    return BilateralUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        sets=sets,
        variant=raw_unit.options.get("variant", "default"),
    )
