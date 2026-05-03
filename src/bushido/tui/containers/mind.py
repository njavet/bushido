from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import TabbedContent, TabPane

from bushido.tui.containers.wimhof import WimhofContainer


class MindContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("wimhof"):
                yield WimhofContainer()
