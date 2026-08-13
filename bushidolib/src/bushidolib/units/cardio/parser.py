from bushidolib.units.dt_parse import (
    parse_military_time_string,
    time_string_to_seconds,
)
from bushidolib.exceptions import ParsingError

from .spec import Data


def parse_cardio_unit(tokens: tuple[str, ...]) -> Data:
    start_t = parse_military_time_string(tokens[0])
    seconds = time_string_to_seconds(tokens[1])
    try:
        location = tokens[2]
    except IndexError as e:
        raise ParsingError("no location") from e

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

    return Data(
        start_t=start_t,
        seconds=seconds,
        location=location,
        distance=distance,
        avg_hr=avg_hr,
        max_hr=max_hr,
        calories=calories,
    )
