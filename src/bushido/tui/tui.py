from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from bushido.categories import LogUnitService, SessionFactory
from bushido.categories.unit_help import UnitHelpService
from bushido.tui.containers.header import HeaderContainer
from bushido.tui.containers.mind import MindContainer
from bushido.tui.containers.training import TrainingContainer
from bushido.tui.containers.work import WorkContainer
from bushido.tui.screens.log_unit import LogUnitScreen


class BushidoApp(App[None]):
    CSS_PATH = "main.tcss"
    BINDINGS = [
        Binding("q", "quit", "quit"),
        Binding("l", "log_unit", "log"),
    ]

    def __init__(
        self,
        session_factory: SessionFactory,
        log_unit_service: LogUnitService,
        unit_help_service: UnitHelpService,
    ) -> None:
        super().__init__()
        self.sf = session_factory
        self.log_unit_service = log_unit_service
        self.unit_help_service = unit_help_service

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
        yield Footer(id="app_footer")

    def action_log_unit(self) -> None:
        # TODO update other widgets after saving a unit
        self.push_screen(LogUnitScreen(self.unit_help_service))

    async def log_unit(self, line: str) -> str | None:
        with self.sf.session() as session:
            error = self.log_unit_service.log_unit(line, session)
        return error
