import datetime
from typing import Literal

from citadel.bcl import LogUnitCommand
from citadel.exceptions import UnitParsingError
from citadel.unit.base import BaseUnit, UnitType


class LogUnit(BaseUnit):
    unit_type: Literal[UnitType.log] = UnitType.log
    kind: str


def build_log_unit(raw_unit: LogUnitCommand, log_time: datetime.datetime) -> LogUnit:
    try:
        kind = raw_unit.args[0]
    except IndexError as e:
        raise UnitParsingError(f"no Kind{raw_unit.unit_name}") from e

    return LogUnit(
        name=raw_unit.unit_name,
        kind=kind,
        log_time=log_time,
        comment=raw_unit.comment,
    )
