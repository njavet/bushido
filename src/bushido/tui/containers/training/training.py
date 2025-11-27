from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    TabbedContent,
    TabPane,
)

from bushido.tui.containers.training.cardio import CardioContainer
from bushido.tui.containers.training.lifting import LiftingContainer


class TrainingContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("lifting"):
                yield LiftingContainer()
            with TabPane("cardio"):
                yield CardioContainer()
