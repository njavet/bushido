import datetime

from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import (
    parse_military_time_string,
    time_string_to_seconds,
)
from bushidolib.schema.unit import RawUnit

from ._spec import CardioData, CardioUnit


def parse_cardio_data(tokens: tuple[str, ...]) -> CardioData:
    start_t = parse_military_time_string(tokens[0])
    seconds = time_string_to_seconds(tokens[1])
    try:
        gym = tokens[2]
    except IndexError as e:
        raise UnitParsingError("no martial_arts") from e

    try:
        distance = float(tokens[3])
    except IndexError:
        distance = None
    try:
        avg_hr = int(tokens[4])
    except IndexError:
        avg_hr = None
    try:
        max_hr = int(tokens[5])
    except IndexError:
        max_hr = None
    try:
        calories = int(tokens[6])
    except IndexError:
        calories = None

    return CardioData(
        start_t=start_t,
        seconds=seconds,
        gym=gym,
        distance=distance,
        avg_hr=avg_hr,
        max_hr=max_hr,
        calories=calories,
    )


def build_cardio_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> CardioUnit:
    cardio_data = parse_cardio_data(raw_unit.tokens)
    return CardioUnit(
        name=raw_unit.key,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=cardio_data.start_t,
        seconds=cardio_data.seconds,
        gym=cardio_data.gym,
        distance=cardio_data.distance,
        avg_hr=cardio_data.avg_hr,
        max_hr=cardio_data.max_hr,
        calories=cardio_data.calories,
    )
