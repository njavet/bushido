from typing import override

from textual.app import ComposeResult
from textual.widget import Widget

from ronin.widgets.command_line import CommandLine
from ronin.widgets.shell_view import ShellView


class Shell(Widget):
    def __init__(self, commands: list[str]) -> None:
        super().__init__()
        self.commands = commands

    @override
    def compose(self) -> ComposeResult:
        yield CommandLine(self.commands)
        yield ShellView()
