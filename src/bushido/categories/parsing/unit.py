import datetime

from bushido.core.dtypes import RawUnit

from ..protocols import Clock
from .dt_parse import parse_datetime


def parse_raw_unit(line: str) -> RawUnit:
    body, sep, comment = line.partition("#")
    tokens = tuple(body.split())

    if not tokens:
        raise ValueError("Empty unit line")

    return RawUnit(
        name=tokens[0],
        tokens=tokens[1:],
        comment=comment.strip() if sep and comment.strip() else None,
    )


def split_options(
    tokens: tuple[str, ...], clock: Clock
) -> tuple[tuple[str, ...], datetime.datetime]:
    clean: list[str] = []
    log_time: datetime.datetime | None = None

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == "--dt":
            if i + 1 >= len(tokens):
                raise ValueError("--dt requires a value")

            log_time = parse_datetime(tokens[i + 1])
            i += 2
            continue

        clean.append(token)
        i += 1
    return tuple(clean), log_time or clock.now()
