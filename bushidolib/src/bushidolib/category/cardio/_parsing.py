from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import (
    parse_military_time_string,
    time_string_to_seconds,
)

from ._spec import CardioUnit
from ..base import RawUnit


def parse_cardio_unit(raw_unit: RawUnit) -> CardioUnit:
    start_t = parse_military_time_string(raw_unit.tokens[0])
    seconds = time_string_to_seconds(raw_unit.tokens[1])
    try:
        gym = raw_unit.tokens[2]
    except IndexError as e:
        raise UnitParsingError("no gym") from e

    try:
        distance = float(raw_unit.tokens[3])
    except IndexError:
        distance = None
    try:
        avg_hr = int(raw_unit.tokens[4])
    except IndexError:
        avg_hr = None
    try:
        max_hr = int(raw_unit.tokens[5])
    except IndexError:
        max_hr = None
    try:
        calories = int(raw_unit.tokens[6])
    except IndexError:
        calories = None

    return CardioUnit(
        name=raw_unit.name,
        start_t=start_t,
        seconds=seconds,
        gym=gym,
        distance=distance,
        avg_hr=avg_hr,
        max_hr=max_hr,
        calories=calories,
    )
