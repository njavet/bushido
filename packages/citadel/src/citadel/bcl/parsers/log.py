from dataclasses import dataclass

from citadel.bcl.errors import CommandSyntaxError


@dataclass(frozen=True, slots=True)
class LogUnitCommand:
    unit_name: str
    args: tuple[str, ...]
    options: dict[str, str]
    flags: list[str]
    comment: str | None


def log_parser(line: str, separator: str = "#") -> LogUnitCommand:
    line = line.strip()
    if not line:
        raise CommandSyntaxError("empty command")
    structured, _, comment = line.partition(separator)
    tokens = structured.split()
    if not tokens:
        raise CommandSyntaxError("missing command")

    args = []
    flags = []
    options = {}
    for token in tokens[1:]:
        if token.startswith(("-", "--")):
            t = token.lstrip("-")
            if "=" in t:
                key, value = t.split("=", 1)
                if key in options:
                    raise CommandSyntaxError(f"duplicated option {token}")
                options[key] = value
            elif t in flags:
                raise CommandSyntaxError(f"duplicated flag {token}")
            else:
                flags.append(token)
        else:
            args.append(token)
    return LogUnitCommand(
        unit_name=tokens[0],
        args=tuple(args),
        options=options,
        flags=flags,
        comment=comment.strip() if comment else None,
    )
