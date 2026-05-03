
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from bushido.categories import LogUnitService, SessionFactory
from bushido.tui.containers.header import HeaderContainer
from bushido.tui.containers.mind import MindContainer
from bushido.tui.containers.training import TrainingContainer
from bushido.tui.containers.work import WorkContainer
from bushido.tui.screens.helpscreen import HelpScreen
from bushido.tui.screens.log_unit import LogUnitScreen


class BushidoApp(App[None]):
    BINDINGS = [
        Binding("q", "quit", "quit"),
        Binding("h", "help", "help"),
        Binding("t", "toggle_tree", "toggle tree"),
        Binding("g", "unit_timeline", "timeLine"),
        Binding("l", "log_unit", "log"),
    ]
    CSS_PATH = "main.tcss"

    def __init__(
        self, session_factory: SessionFactory, log_unit_service: LogUnitService
    ) -> None:
        super().__init__()
        self.sf = session_factory
        self.log_unit_service = log_unit_service

    def compose(self) -> ComposeResult:
        yield HeaderContainer()
        yield Rule()
        with TabbedContent():
            with TabPane("training"):
                yield TrainingContainer()
            with TabPane("mind"):
                yield MindContainer()
            with TabPane("work"):
                yield WorkContainer()
        yield Footer()

    def action_log_unit(self) -> None:
        # TODO update other widgets after saving a unit
        self.push_screen(LogUnitScreen(self.log_unit_service, self.sf))

    def action_help(self) -> None:
        self.push_screen(HelpScreen())
