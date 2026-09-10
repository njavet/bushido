import datetime
from dataclasses import dataclass
from pydantic import BaseModel

from bushidolib.category.cardio import CardioData
from bushidolib.category.gym import GymData
from bushidolib.category.lifting import LiftingData
from bushidolib.category.wimhof import WimhofData
from bushidolib.exceptions import UnitParsingError


UnitData = CardioData | GymData | LiftingData | WimhofData


class Unit(BaseModel):
    name: str
    log_time: datetime.datetime
    data: UnitData
    comment: str | None = None


@dataclass(frozen=True, slots=True)
class RawUnit:
    name: str
    tokens: tuple[str, ...]
    log_time_str: str | None = None
    comment: str | None = None


def parse_raw_unit(line: str) -> RawUnit:
    body, sep, comment = line.partition("#")
    raw_tokens = tuple(body.split())
    if not raw_tokens:
        raise UnitParsingError(f"Empty unit line: {line}")
    tokens, log_time_str = split_options(raw_tokens)
    return RawUnit(
        name=tokens[0],
        tokens=tokens[1:],
        log_time_str=log_time_str,
        comment=comment.strip() if sep and comment.strip() else None,
    )


def split_options(tokens: tuple[str, ...]) -> tuple[tuple[str, ...], str | None]:
    clean: list[str] = []
    log_time: str | None = None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "--dt":
            if i + 1 >= len(tokens):
                raise UnitParsingError("--dt requires a value")
            log_time = tokens[i + 1]
            i += 2
            continue
        clean.append(token)
        i += 1
    return tuple(clean), log_time
