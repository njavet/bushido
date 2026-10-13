from dataclasses import dataclass

from .errors import CommandSyntaxError


@dataclass(frozen=True, slots=True)
class PreparsedCommand:
    name: str
    body: str
    comment: str | None


def preparse(line: str, separator: str = "#") -> PreparsedCommand:
    line = line.strip()

    if not line:
        raise CommandSyntaxError("empty command")

    structured, comment_sep, free_text = line.partition(separator)
    structured = structured.strip()

    if not structured:
        raise CommandSyntaxError("missing command")

    name, _, body = structured.partition(" ")

    return PreparsedCommand(
        name=name,
        body=body.strip(),
        comment=free_text.strip() if comment_sep else None,
    )
