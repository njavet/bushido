import datetime
from dataclasses import dataclass
from enum import StrEnum

from bushido.core.result import Err, Ok, Result

from ..parsing.base import UnitParser
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
class GymParser(UnitParser[GymSpec]):
    grammar = """
<name> <start>-<end> <location> [<training>] [<focus>] # [<comment>]

name:
  weights | martial_arts | yoga

time:
  HHMM-HHMM
"""
    unit_names = [unit_name.value for unit_name in GymUnitName]

    @staticmethod
    def parse(tokens: tuple[str, ...]) -> Result[GymSpec]:
        res_t = parse_start_end_time_string(tokens[0])
        if isinstance(res_t, Err):
            return res_t

        start_t, end_t = res_t.value
        try:
            location = tokens[1]
        except IndexError:
            return Err("no unit location")
        try:
            training = tokens[2]
        except IndexError:
            training = None
        try:
            focus = tokens[3]
        except IndexError:
            focus = None

        data = GymSpec(
            start_t=start_t,
            end_t=end_t,
            location=location,
            training=training,
            focus=focus,
        )
        return Ok(data)
