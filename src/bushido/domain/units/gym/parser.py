from dataclasses import dataclass

from ..dt_parse import parse_start_end_time_string
from ..exceptions import ParsingError
from .spec import Data


@dataclass(frozen=True, slots=True)
class Parser:
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> Data:
        start_t, end_t = parse_start_end_time_string(tokens[0])
        try:
            location = tokens[1]
        except IndexError:
            raise ParsingError("no location")

        return Data(
            start_t=start_t,
            end_t=end_t,
            gym=location,
            training=None,
            focus=None,
        )
