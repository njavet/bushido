import datetime
from dataclasses import dataclass
from enum import StrEnum

from ..exceptions import ParsingError
from ..parsing.dt_parse import parse_start_end_time_string


class GymUnitName(StrEnum):
    weights = "weights"
    martial_arts = "martial_arts"
    yoga = "yoga"


@dataclass(frozen=True, slots=True)
class GymSpec:
    start_t: datetime.time
    end_t: datetime.time
    location: str
    training: str | None = None
    focus: str | None = None


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
            location=location,
            training=training,
            focus=focus,
        )
