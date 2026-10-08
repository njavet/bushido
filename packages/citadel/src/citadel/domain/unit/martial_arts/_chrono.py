import datetime
from typing import Literal

from citadel.domain.unit._base import BaseUnit, RawUnit, UnitType
from citadel.exceptions import UnitParsingError


class ChronoUnit(BaseUnit):
    unit_type: Literal[UnitType.chrono] = UnitType.chrono
    seconds: float


def parse_chrono_data(tokens: tuple[str, ...]) -> float:
    try:
        return float(tokens[0])
    except ValueError as e:
        raise UnitParsingError("invalid seconds") from e


def build_chrono_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> ChronoUnit:
    seconds = parse_chrono_data(raw_unit.tokens)
    return ChronoUnit(
        name=raw_unit.name, log_time=log_time, comment=raw_unit.comment, seconds=seconds
    )
