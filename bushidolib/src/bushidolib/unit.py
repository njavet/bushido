import datetime
from dataclasses import dataclass

from pydantic import BaseModel

from bushidolib.constants import UnitCategory
from bushidolib.exceptions import UnitParsingError
from bushidolib.registry import UNIT_TYPE_REGISTRY, UnitData


class Unit(BaseModel):
    name: str
    log_time: datetime.datetime
    data: UnitData
    comment: str | None = None


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None


def build_unit(
    raw_unit: RawUnit, category: UnitCategory, log_time: datetime.datetime
) -> Unit:
    parse_fn = UNIT_TYPE_REGISTRY[category]
    return Unit(
        name=raw_unit.name,
        log_time=log_time,
        data=parse_fn(raw_unit.tokens),
        comment=raw_unit.comment,
    )


def parse_raw_unit(line: str) -> RawUnit:
    body, sep, comment = line.partition("#")
    raw_tokens = tuple(body.split())
    if not raw_tokens:
        raise UnitParsingError(f"Empty unit line: {line}")
    return RawUnit(
        name=raw_tokens[0],
        tokens=raw_tokens[1:],
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
