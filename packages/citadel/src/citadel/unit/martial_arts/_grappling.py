import datetime

from citadel.exceptions import UnitParsingError
from citadel.bcl import LogUnitCommand
from citadel.unit.parsing import parse_start_end_time_string

from ._base import MartialArtsUnit


def build_grappling_unit(
    raw_unit: LogUnitCommand, log_time: datetime.datetime
) -> MartialArtsUnit:
    start_t, end_t = parse_start_end_time_string(raw_unit.args[0])
    try:
        gym = raw_unit.args[1]
    except IndexError as e:
        raise UnitParsingError("no gym") from e
    return MartialArtsUnit(
        name=raw_unit.unit_name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=start_t,
        end_t=end_t,
        gym=gym,
    )
