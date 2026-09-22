import datetime
from typing import Self

from pydantic import BaseModel, Field

from bushidolib.constants import UnitCategory
from bushidolib.exceptions import UnitParsingError


class LogUnitRequest(BaseModel):
    line: str = Field(min_length=1)


class LoadUnitRequest(BaseModel):
    unit_category: UnitCategory
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None


class RawUnit(BaseModel):
    key: str
    tokens: tuple[str, ...]
    raw_log_time: str | None = None
    comment: str | None = None

    @classmethod
    def from_line(cls, line: str) -> Self:
        parts = line.split("#")
        raw_tokens = tuple(parts[0].split())
        if not raw_tokens:
            raise UnitParsingError(f"Empty unit line: {line}")

        try:
            comment = parts[1].strip()
        except IndexError:
            comment = None

        try:
            raw_log_time = parts[2].strip()
        except IndexError:
            raw_log_time = None

        return cls(
            key=raw_tokens[0],
            tokens=raw_tokens[1:],
            raw_log_time=raw_log_time,
            comment=comment,
        )


class BaseUnit(BaseModel):
    name: str
    log_time: datetime.datetime
    comment: str | None = None


class SpaceTimeData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str


class ChronoData(BaseModel):
    seconds: float
