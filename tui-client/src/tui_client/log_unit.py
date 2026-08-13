import datetime
from functools import singledispatch

from sqlalchemy.orm import Session

from bushido_server.dtypes import Clock, SystemClock
from bushido_server.schema.log_req import CardioLogUnitRequest
from bushidolib.exceptions import ParsingError
from bushidolib.units import Unit



def parse_raw_unit(line: str) -> tuple[str, tuple[str, ...], str | None]:
    body, sep, comment = line.partition("#")
    tokens = tuple(body.split())

    if not tokens:
        raise ParsingError(f"Empty unit line: {line}")

    name=tokens[0]
    tokens=tokens[1:]
    comment=comment.strip() if sep and comment.strip() else None
    return name, tokens, comment


def split_options(tokens: tuple[str, ...]) -> tuple[tuple[str, ...], str | None]:
    clean: list[str] = []
    log_time: str | None = None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "--dt":
            if i + 1 >= len(tokens):
                raise ParsingError("--dt requires a value")
            log_time = tokens[i + 1]
            i += 2
            continue
        clean.append(token)
        i += 1
    return tuple(clean), log_time
