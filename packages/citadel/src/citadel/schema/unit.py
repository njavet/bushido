from typing import Self

from pydantic import BaseModel


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    flags: list[str]
    options: dict[str, str]
    comment: str | None = None

    @classmethod
    def from_line(cls, line: str) -> Self:
        payload, sep, comment = line.partition(COMMENT_SEP)
        words = tuple(payload.split())
        result = split_words(words)
        if not result.tokens:
            raise UnitParsingError(f"Empty unit line: {line}")
        return cls(
            name=result.tokens[0],
            tokens=result.tokens[1:],
            flags=result.flags,
            options=result.options,
            comment=comment.strip() if sep and comment.strip() else None,
        )

