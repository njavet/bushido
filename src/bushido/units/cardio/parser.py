from bushido.core.result import Err, Ok, Result
from bushido.units.parsing.base import UnitParser
from bushido.units.parsing.dt_parse import (
    parse_military_time_string,
    time_string_to_seconds,
)

from .domain import CardioSpec


class CardioParser(UnitParser[CardioSpec]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> Result[CardioSpec]:

        res_t = parse_military_time_string(tokens[0])
        if isinstance(res_t, Err):
            return res_t

        start_t = res_t.value
        res_s = time_string_to_seconds(tokens[1])
        if isinstance(res_s, Err):
            return Err("no time")

        seconds = res_s.value
        try:
            location = tokens[2]
        except IndexError:
            return Err("no location")

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

        data = CardioSpec(
            start_t=start_t,
            seconds=seconds,
            location=location,
            distance=distance,
            avg_hr=avg_hr,
            max_hr=max_hr,
            calories=calories,
        )
        return Ok(data)
