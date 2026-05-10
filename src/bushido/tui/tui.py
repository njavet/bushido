from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from bushido.categories import UnitService
from bushido.infra.db import SessionFactory
from bushido.tui.containers import GymContainer, HeaderContainer
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
            with TabPane("training"):
                yield GymContainer(id="gym_container")
        yield Footer(id="app_footer")

    def on_mount(self) -> None:
        self.update_gym_container()

    def update_gym_container(self) -> None:
        gc = self.query_one("#gym_container", GymContainer)
        with self.sf.session() as session:
            units = self.unit_service.load_training_units(session)
        gc.set_units(units)

    def action_log_unit(self) -> None:
        # TODO update other widgets after saving a unit
        self.push_screen(LogUnitScreen(self.unit_service, self.log_unit))

    async def log_unit(self, line: str) -> str | None:
        with self.sf.session() as session:
            error = self.unit_service.log_unit(line, session)
        return error
