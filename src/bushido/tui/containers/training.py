from typing import Any

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    Markdown,
    TabbedContent,
    TabPane,
)


class TrainingContainer(Container):
    def __init__(self, units: dict[str, Any]) -> None:
        super().__init__()
        self.units = units

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("stats"):
                yield Markdown("TODO")
            with TabPane("lifting"):
                yield LiftingContainer()
            with TabPane("cardio"):
                yield CardioContainer()


class LiftingContainer(Container):
    def compose(self) -> ComposeResult:
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


class CardioContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("running"):
                yield Markdown("TODO")
            with TabPane("swimming"):
                yield Markdown("TODO")
            with TabPane("skipping"):
                yield Markdown("TODO")
