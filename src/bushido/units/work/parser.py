import datetime
from dataclasses import dataclass
from enum import StrEnum

from bushido.core.result import Err, Ok, Result

from ..parsing.base import UnitParser
from ..parsing.dt_parse import parse_start_end_time_string


class WorkUnitName(StrEnum):
    risktec = "risktec"
    myself = "myself"


@dataclass(frozen=True, slots=True)
class WorkSpec:
    start_t: datetime.time
    end_t: datetime.time
    location: str
    employer: str
    project: str


@dataclass(frozen=True, slots=True)
class WorkParser(UnitParser[WorkSpec]):
    grammar = ""
    unit_names = [unit_name.value for unit_name in WorkUnitName]

    @staticmethod
    def parse(tokens: tuple[str, ...]) -> Result[WorkSpec]:
        res_t = parse_start_end_time_string(tokens[0])
        if isinstance(res_t, Err):
            return res_t

        start_t, end_t = res_t.value
        try:
            location = tokens[1]
        except IndexError:
            return Err("no unit location")
        try:
            employer = tokens[2]
        except IndexError:
            return Err("no unit employer")
        try:
            project = tokens[3]
        except IndexError:
            return Err("no unit project")

        data = WorkSpec(
            start_t=start_t,
            end_t=end_t,
            location=location,
            employer=employer,
            project=project,
        )
        return Ok(data)
