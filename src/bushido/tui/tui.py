from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from bushido.db.sf import SessionFactory
from bushido.service import UnitService
from bushido.tui.containers import HeaderContainer, LiftingContainer
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
        unit_service: UnitService,
    ) -> None:
        super().__init__()
        self.sf = session_factory
        self.unit_service = unit_service

    def compose(self) -> ComposeResult:
        yield HeaderContainer()
        yield Rule()
        with TabbedContent(id="main_tabs"):
            with TabPane("lifting"):
                yield LiftingContainer(id="lifting_container")

        yield Footer(id="app_footer")

    def on_mount(self) -> None:
        self.update_lifting_container()

    def update_lifting_container(self) -> None:
        gc = self.query_one("#lifting_container", LiftingContainer)
        with self.sf.session() as session:
            units = self.unit_service.load_lifting_units(session)
            gc.set_units(units)

    def action_log_unit(self) -> None:
        # TODO update other widgets after saving a units
        self.push_screen(LogUnitScreen(self.unit_service, self.log_unit))

    async def log_unit(self, line: str) -> None:
        with self.sf.session() as session:
            self.unit_service.log_unit(line, session)
