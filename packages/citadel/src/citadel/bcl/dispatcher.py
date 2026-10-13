class CommandDispatcher:
    def __init__(self, unit_names: frozenset[str]) -> None:
        self.unit_names = unit_names

        self.parsers: dict[str, CommandParser] = {
            "find": parse_find,
            "stats": parse_stats,
            "progress": parse_progress,
        }

    def parse(self, line: str) -> Command:
        raw = preparse(line)

        if raw.name in self.unit_names:
            return self._parse_unit(raw)

        try:
            parser = self.parsers[raw.name]
        except KeyError:
            raise UnknownCommandError(
                f"unknown command: {raw.name}"
            ) from None

        return parser(raw)

    def _parse_unit(
        self,
        raw: PreparsedCommand,
    ) -> LogUnitCommand:
        structured_line = raw.name

        if raw.body:
            structured_line += f" {raw.body}"

        return LogUnitCommand(
            unit_name=raw.name,
            line=structured_line,
            comment=raw.comment,
        )