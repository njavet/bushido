import datetime
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bushido.core.dtypes import (
    Clock,
    Options,
    ParsedUnit,
    RawUnit,
    SystemClock,
    UnitData,
)

T = TypeVar("T", bound=UnitData)


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


class TokenParser(ABC, Generic[T]):
    @abstractmethod
    def parse_tokens(self, tokens: tuple[str, ...]) -> T: ...


class UnitParser:
    def __init__(
        self, parsers: dict[str, TokenParser[object]], clock: Clock = SystemClock()
    ) -> None:
        self.parsers = parsers
        self.clock = clock

    def split_options(self, tokens: tuple[str, ...]) -> tuple[tuple[str, ...], Options]:
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
        return tuple(clean), Options(log_time=log_time or self.clock.now())

    def parse(self, line: str) -> ParsedUnit[object]:
        raw = parse_raw_unit(line)
        try:
            parser = self.parsers[raw.name]
        except KeyError:
            raise ValueError(f"Unknown unit: {raw.name}") from None
        payload_tokens, options = self.split_options(raw.tokens[1:])

        return ParsedUnit(
            name=raw.name,
            data=parser.parse_tokens(payload_tokens),
            options=options,
            comment=raw.comment,
        )
