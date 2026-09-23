import datetime
from typing import Self

from pydantic import BaseModel, Field

from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import split_words


class LogUnitRequest(BaseModel):
    line: str = Field(min_length=1)


class LoadUnitRequest(BaseModel):
    unit_name: str
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    flags: list[str]
    options: dict[str, str]
    comment: str | None = None

    @classmethod
    def from_line(cls, line: str) -> Self:
        parts = line.split("#")
        words = tuple(parts[0].split())
        if not words:
            raise UnitParsingError(f"Empty unit line: {line}")
        try:
            comment = parts[1].strip()
        except IndexError:
            comment = None
        result = split_words(words[1:])
        return cls(
            name=words[0],
            tokens=result.tokens,
            flags=result.flags,
            options=result.options,
            comment=comment,
        )


class BaseUnit(BaseModel):
    log_time: datetime.datetime
    comment: str | None = None


class SpaceTimeData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
