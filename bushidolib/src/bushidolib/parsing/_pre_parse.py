from bushidolib.exceptions import UnitParsingError
from bushidolib.unit import RawUnit


def parse_raw_unit(line: str) -> RawUnit:
    body, sep, comment = line.partition("#")
    tokens = tuple(body.split())

    if not tokens:
        raise UnitParsingError(f"Empty unit line: {line}")

    name = tokens[0]
    tokens = tokens[1:]
    comment_ = comment.strip() if sep and comment.strip() else None
    return RawUnit(name=name, tokens=tokens, comment=comment_)


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
