import datetime

from bushidolib.exceptions import UnitParsingError
from bushidolib.unit.base import BaseUnit, RawUnit


class LogUnit(BaseUnit):
    name: str
    kind: str


def build_log_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> LogUnit:
    try:
        kind = raw_unit.tokens[0]
    except IndexError:
        raise UnitParsingError(f"no Kind{raw_unit.name}")

    return LogUnit(name=raw_unit.name,
                   kind=kind,
                   log_time=log_time,
                   comment=raw_unit.comment,
    )
