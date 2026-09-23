import datetime

from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import parse_start_end_time_string
from bushidolib.unit.base import BaseUnit, RawUnit, SpaceTimeData


class MartialArtsUnit(BaseUnit, SpaceTimeData):
    kind: str


def build_martial_arts_unit(
    raw_unit: RawUnit, log_time: datetime.datetime
) -> MartialArtsUnit:
    start_t, end_t = parse_start_end_time_string(raw_unit.tokens[0])
    try:
        gym = raw_unit.tokens[1]
    except IndexError as e:
        raise UnitParsingError("no gym") from e
    return MartialArtsUnit(
        kind=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=start_t,
        end_t=end_t,
        gym=gym,
    )
