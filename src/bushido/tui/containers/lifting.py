
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    Markdown,
    TabbedContent,
    TabPane,
)


class LiftingContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("stats"):
                yield Markdown("TODO")
            with TabPane("squat"):
                yield Markdown("TODO")
            with TabPane("deadlift"):
                yield Markdown("TODO")
            with TabPane("benchpress"):
                yield Markdown("TODO")
            with TabPane("overheadpress"):
                yield Markdown("TODO")
            with TabPane("rows"):
                yield Markdown("TODO")
