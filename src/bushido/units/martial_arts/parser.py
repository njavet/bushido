from dataclasses import dataclass

from bushido.units.dt_parse import parse_start_end_time_string
from bushido.units.exceptions import ParsingError

from .unit import LiftingData


@dataclass(frozen=True, slots=True)
class LiftingParser:
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> LiftingData:
        start_t, end_t = parse_start_end_time_string(tokens[0])
        try:
            location = tokens[1]
        except IndexError:
            raise ParsingError("no location")

        return LiftingData(
            start_t=start_t,
            end_t=end_t,
            gym=location,
            training=None,
            focus=None,
        )
