from typing import Self
import datetime

from pydantic import model_validator

from bushidolib.exceptions import UnitParsingError
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
    return WorkUnit(
        log_time=log_time,
        comment=raw_unit.comment,
    )
