import datetime

from bushidolib.contracts.unit import RawUnit
from bushidolib.exceptions import ParsingUnitError


def parse_raw_unit(line: str) -> RawUnit:
    body, sep, comment = line.partition("#")
    tokens = tuple(body.split())

    if not tokens:
        raise ParsingUnitError(f"Empty unit line: {line}")

    name = tokens[0]
    tokens = tokens[1:]
    comment_ = comment.strip() if sep and comment.strip() else None
    return RawUnit(name=name, tokens=tokens, comment=comment_)


def split_options(
    tokens: tuple[str, ...], timezone: datetime.tzinfo
) -> tuple[tuple[str, ...], datetime.datetime | None]:
    clean: list[str] = []
    log_time: datetime.datetime | None = None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "--dt":
            if i + 1 >= len(tokens):
                raise ParsingUnitError("--dt requires a value")
            try:
                log_time = datetime.datetime.strptime(
                    tokens[i + 1], "%Y%m%d-%H%M"
                ).replace(tzinfo=timezone)
            except ValueError as e:
                raise ParsingUnitError(
                    f"invalid datetime format: {tokens[i + 1]}"
                ) from e
            i += 2
            continue
        clean.append(token)
        i += 1
    return tuple(clean), log_time
