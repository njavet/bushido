import datetime

from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import parse_start_end_time_string
from bushidolib.schema.unit import RawUnit

from ._spec import GymData, GymUnit


def parse_gym_data(tokens: tuple[str, ...]) -> GymData:
    start_t, end_t = parse_start_end_time_string(tokens[0])
    try:
        gym = tokens[1]
    except IndexError as e:
        raise UnitParsingError("no martial_arts") from e

    return GymData(
        start_t=start_t,
        end_t=end_t,
        gym=gym,
    )


def build_gym_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> GymUnit:
    gym_data = parse_gym_data(raw_unit.tokens)
    return GymUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=gym_data.start_t,
        end_t=gym_data.end_t,
        gym=gym_data.gym,
    )
