from dataclasses import dataclass

from ..exceptions import ParsingError
from ..parsing.dt_parse import parse_start_end_time_string
from ..unit_settings import GymUnitName
from .domain import GymSpec


@dataclass(frozen=True, slots=True)
class GymParser:
    grammar = """
        <name> <start>-<end> <location> [<training>] [<focus>] # [<comment>]
        
        time format:
          HHMM-HHMM
    """
    unit_names = [unit_name.value for unit_name in GymUnitName]

    @staticmethod
    def parse(tokens: tuple[str, ...]) -> GymSpec:
        start_t, end_t = parse_start_end_time_string(tokens[0])
        try:
            location = tokens[1]
        except IndexError:
            raise ParsingError("no location")
        try:
            training = tokens[2]
        except IndexError:
            training = None
        try:
            focus = tokens[3]
        except IndexError:
            focus = None

        return GymSpec(
            start_t=start_t,
            end_t=end_t,
            gym=location,
            training=training,
            focus=focus,
        )
