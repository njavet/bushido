from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    Markdown,
    TabbedContent,
    TabPane,
)


class CardioContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("stats"):
                yield Markdown("TODO")
            with TabPane("running"):
                yield Markdown("TODO")
            with TabPane("swimming"):
                yield Markdown("TODO")
            with TabPane("skipping"):
                yield Markdown("TODO")
