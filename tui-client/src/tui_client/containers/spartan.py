from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    RichLog,
)


class SpartanContainer(Container):
    def compose(self) -> ComposeResult:
        yield RichLog()
