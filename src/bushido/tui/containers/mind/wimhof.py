from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    Markdown,
)


class WimhofContainer(Container):
    def compose(self) -> ComposeResult:
        yield Markdown("TODO")
