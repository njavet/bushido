from typing import Self
import datetime

from pydantic import model_validator

from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import parse_start_end_time_string, time_string_to_seconds
from bushidolib.unit.base import BaseUnit, RawUnit


class WorkUnit(BaseUnit):
    start_t: datetime.time | None = None
    end_t: datetime.time | None = None
    seconds: float | None = None
    gym: str
    project: str
    topic: str

    @model_validator(mode="after")
    def check_at_least_one(self) -> Self:
        if self.seconds:
            cond0 = self.start_t is None
            cond1 = self.end_t is None
            if not cond0 or not cond1:
                raise UnitParsingError(f"if time is specified, do not provide start and end time")
        else:
            if self.start_t is None:
                raise UnitParsingError(f"no start time")
            if self.end_t is None:
                raise UnitParsingError(f"no end time")
            if self.end_t <= self.start_t:
                raise UnitParsingError(f"end time is before start time")
        return self


def build_work_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> WorkUnit:
    try:
        start_t, end_t = parse_start_end_time_string(raw_unit.tokens[0])
    except UnitParsingError:
        start_t, end_t = None, None
        try:
            seconds = time_string_to_seconds(raw_unit.tokens[0])
        except Exception as e:
            raise UnitParsingError(f"failed to parse time string: {e}") from e
    else:
        seconds = None
    try:
        gym = raw_unit.tokens[1]
    except IndexError:
        raise UnitParsingError(f"failed to parse gym string: {raw_unit.tokens}")
    try:
        project = raw_unit.tokens[2]
    except IndexError:
        raise UnitParsingError(f"failed to parse project string: {raw_unit.tokens}")
    try:
        topic = raw_unit.tokens[3]
    except IndexError:
        raise UnitParsingError(f"failed to parse topic string: {raw_unit.tokens}")

    return WorkUnit(
        start_t=start_t,
        end_t=end_t,
        seconds=seconds,
        gym=gym,
        project=project,
        topic=topic,
        log_time=log_time,
        comment=raw_unit.comment,
    )
