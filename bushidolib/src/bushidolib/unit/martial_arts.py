import datetime

from bushidolib.parsing import parse_space_time_data
from bushidolib.unit.base import BaseUnit, RawUnit, SpaceTimeData


class MartialArtsUnit(BaseUnit, SpaceTimeData):
    kind: str


def build_martial_arts_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> MartialArtsUnit:
    data = parse_space_time_data(raw_unit.tokens)
    return MartialArtsUnit(
        kind=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=data.start_t,
        end_t=data.end_t,
        gym=data.gym,
    )
