from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from bushido.infra.db import SessionFactory
from bushido.service import UnitService
from bushido.tui.containers import BarbellContainer, HeaderContainer
from bushido.tui.screens.log_unit import LogUnitScreen


class BushidoApp(App[None]):
    CSS_PATH = "main.tcss"
    BINDINGS = [
        Binding("q", "quit", "quit"),
        Binding("l", "log_unit", "log"),
        Binding("escape", "cancel", "cancel"),
    ]

    def __init__(
        self,
        session_factory: SessionFactory,
        unit_log_service: UnitService,
    ) -> None:
        super().__init__()
        self.sf = session_factory
        self.unit_log_service = unit_log_service

    def compose(self) -> ComposeResult:
        yield HeaderContainer()
        yield Rule()
        with TabbedContent(id="main_tabs"):
            with TabPane("barbell"):
                yield BarbellContainer(id="lifting_container")

        yield Footer(id="app_footer")

    def action_log_unit(self) -> None:
        # TODO update other widgets after saving a units
        self.push_screen(LogUnitScreen(self.unit_log_service, self.log_unit))

    async def log_unit(self, line: str) -> None:
        with self.sf.session() as session:
            self.unit_log_service.log_unit(line, session)
