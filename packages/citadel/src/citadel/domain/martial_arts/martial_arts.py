import datetime

from citadel.domain.base import BaseUnit, RawUnit, SpaceTimeData
from citadel.domain.parsing import parse_start_end_time_string
from citadel.exceptions import UnitParsingError


class MartialArtsUnit(BaseUnit, SpaceTimeData):
    pass


def build_martial_arts_unit(
    raw_unit: RawUnit, log_time: datetime.datetime
) -> MartialArtsUnit:
    start_t, end_t = parse_start_end_time_string(raw_unit.tokens[0])
    try:
        gym = raw_unit.tokens[1]
    except IndexError as e:
        raise UnitParsingError("no gym") from e
    return MartialArtsUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=start_t,
        end_t=end_t,
        gym=gym,
    )
