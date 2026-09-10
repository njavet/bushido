
from bushidolib.exceptions import UnitParsingError

from ._spec import RawUnit


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
