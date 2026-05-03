import datetime
from dataclasses import dataclass
from enum import StrEnum

from ..exceptions import ParsingError
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
class WorkParser:
    grammar = ""
    unit_names = [unit_name.value for unit_name in WorkUnitName]

    @staticmethod
    def parse(tokens: tuple[str, ...]) -> WorkSpec:
        start_t, end_t = parse_start_end_time_string(tokens[0])
        try:
            location = tokens[1]
        except IndexError:
            raise ParsingError("no location")
        try:
            employer = tokens[2]
        except IndexError:
            raise ParsingError("no employer")
        try:
            project = tokens[3]
        except IndexError:
            raise ParsingError("no project")

        return WorkSpec(
            start_t=start_t,
            end_t=end_t,
            location=location,
            employer=employer,
            project=project,
        )
