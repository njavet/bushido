import datetime
from typing import Self

from pydantic import BaseModel, Field

from bushidolib.constants import COMMENT_SEP
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
        payload, sep, comment = line.partition(COMMENT_SEP)
        words = tuple(payload.split())
        result = split_words(words)
        if not result.tokens:
            raise UnitParsingError(f"Empty unit line: {line}")
        return cls(
            name=result.tokens[0],
            tokens=result.tokens[1:],
            flags=result.flags,
            options=result.options,
            comment=comment.strip() if sep and comment.strip() else None,
        )


class BaseUnit(BaseModel):
    log_time: datetime.datetime
    comment: str | None = None


class SpaceTimeData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
