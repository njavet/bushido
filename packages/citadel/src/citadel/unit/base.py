import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel

from citadel.constants import COMMENT_SEP, MAX_COMMENT_LENGTH, MAX_FLAGS, MAX_OPTIONS
from citadel.exceptions import UnitParsingError
from citadel.unit.parsing import split_words


class UnitType(StrEnum):
    swimming = "swimming"
    running = "running"
    skipping = "skipping"
    chrono = "chrono"
    log = "log"
    martial_arts = "martial_arts"
    lifting = "lifting"
    barbell = "barbell"
    wimhof = "wimhof"
    work = "work"


class BaseUnit(BaseModel):
    name: str
    log_time: datetime.datetime
    comment: str | None = None


class SpaceTimeData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    flags: list[str]
    options: dict[str, str]
    comment: str | None = None

    @classmethod
    def from_line(cls, line: str) -> Self:
        payload, sep, comment = line.partition(COMMENT_SEP)
        if len(comment) > MAX_COMMENT_LENGTH:
            raise UnitParsingError("comment too long")

        words = tuple(payload.split())
        result = split_words(words)
        if len(result.flags) > MAX_FLAGS:
            raise UnitParsingError("too many flags")
        if len(result.options) > MAX_OPTIONS:
            raise UnitParsingError("too many options")
        if not result.tokens:
            raise UnitParsingError(f"Empty unit line: {line}")
        return cls(
            name=result.tokens[0],
            tokens=result.tokens[1:],
            flags=result.flags,
            options=result.options,
            comment=comment.strip() if sep and comment.strip() else None,
        )
