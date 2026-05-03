import datetime
from abc import ABC, abstractmethod
from typing import Generic

from bushido.core.dtypes import (
    Clock,
    RawUnit,
    TUData,
)
from bushido.core.result import Result


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


def parse_datetime(value: str) -> datetime.datetime:
    return datetime.datetime.strptime(value, "%d.%m.%y-%H%M").replace(
        tzinfo=datetime.UTC
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


class UnitParser(ABC, Generic[TUData]):
    @staticmethod
    @abstractmethod
    def parse(tokens: tuple[str, ...]) -> Result[TUData]: ...
