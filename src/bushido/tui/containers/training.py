from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    Markdown,
    TabbedContent,
    TabPane,
)


class TrainingContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("stats"):
                yield Markdown("TODO")
            with TabPane("lifting"):
                with TabbedContent():
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
            with TabPane("cardio"):
                with TabbedContent():
                    with TabPane("running"):
                        yield Markdown("TODO")
                    with TabPane("swimming"):
                        yield Markdown("TODO")
                    with TabPane("skipping"):
                        yield Markdown("TODO")
