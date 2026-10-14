import datetime
from typing import Literal

from citadel.exceptions import UnitParsingError
from citadel.unit.base import BaseUnit, RawUnit, UnitType


class LogUnit(BaseUnit):
    unit_type: Literal[UnitType.log] = UnitType.log
    kind: str


def build_log_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> LogUnit:
    try:
        kind = raw_unit.tokens[0]
    except IndexError as e:
        raise UnitParsingError(f"no Kind{raw_unit.name}") from e

    return LogUnit(
        name=raw_unit.name,
        kind=kind,
        log_time=log_time,
        comment=raw_unit.comment,
    )
