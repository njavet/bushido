from typing import override

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input, Static


class CommandLine(Widget):
    @override
    def compose(self) -> ComposeResult:
        yield Static("> ", classes="prompt")
        yield Input(id="command-input")
