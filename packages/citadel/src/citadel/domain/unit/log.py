import datetime

from citadel.exceptions import UnitParsingError
from citadel.domain.unit.base import BaseUnit
from citadel.schema.unit import RawUnit


class LogUnit(BaseUnit):
    name: str
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
