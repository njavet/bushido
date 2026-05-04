from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    Markdown,
    TabbedContent,
    TabPane,
)


class GymContainer(Container):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("stats"):
                yield Markdown("TODO")
