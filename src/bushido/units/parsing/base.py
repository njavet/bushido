import datetime
from dataclasses import dataclass
from typing import TypeAlias

Tokens: TypeAlias = list[str]
Comment: TypeAlias = str | None


@dataclass(frozen=True, slots=True)
class ParsedBaseUnit:
    name: str
    tokens: Tokens
    log_time: datetime.datetime
    comment: Comment


def split_line(line: str) -> tuple[Tokens, Comment]:
    parts = line.split("#", 1)
    payload = parts[0].strip()
    try:
        comment = parts[1].strip()
    except IndexError:
        comment = None
    return payload.split(), comment


def parse_base_unit(line: str) -> ParsedBaseUnit:
    pass
