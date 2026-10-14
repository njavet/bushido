from .errors import UnknownCommand
from .parsers.log import LogUnitCommand, log_parser

type Command = LogUnitCommand


def dispatch_command(line: str) -> Command:
    cmd_name, _, rest = line.partition(" ")
    match cmd_name:
        case "log":
            return log_parser(rest)
        case _:
            raise UnknownCommand(f"Unknown command: {cmd_name}")
