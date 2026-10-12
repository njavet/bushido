from typing import override

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import RichLog


class LogsContainer(Container):
    @override
    def compose(self) -> ComposeResult:
        yield RichLog()
