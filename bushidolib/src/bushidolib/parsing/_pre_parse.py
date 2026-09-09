from bushidolib.category.unit import RawUnit
from bushidolib.exceptions import UnitParsingError


def parse_raw_unit(line: str) -> RawUnit:
    body, sep, comment = line.partition("#")
    raw_tokens = tuple(body.split())

    if not raw_tokens:
        raise UnitParsingError(f"Empty unit line: {line}")

    comment_ = comment.strip() if sep and comment.strip() else None
    return split_options(raw_tokens, comment_)


def split_options(raw_tokens: tuple[str, ...], comment: str | None) -> RawUnit:
    tokens: list[str] = []
    options: list[str] = []

    i = 1
    while i < len(raw_tokens):
        token = raw_tokens[i]
        if token.startswith("--"):
            options.append(token)
        else:
            tokens.append(token)
        i += 1

    return RawUnit(
        name=raw_tokens[0], tokens=tuple(tokens), options=options, comment=comment
    )
