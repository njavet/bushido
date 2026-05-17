from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from bushido.persistence.sf import SessionFactory
from bushido.service import LogUnitService
from bushido.service.load_unit_service import LoadUnitService
from bushido.tui.containers import HeaderContainer, LiftingContainer
from bushido.tui.containers.gym import GymContainer
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
        log_unit_service: LogUnitService,
        load_unit_service: LoadUnitService,
    ) -> None:
        super().__init__()
        self.sf = session_factory
        self.log_unit_service = log_unit_service
        self.load_unit_service = load_unit_service

    def compose(self) -> ComposeResult:
        yield HeaderContainer()
        yield Rule()
        with TabbedContent(id="main_tabs"):
            with TabPane("gym"):
                yield GymContainer(id="gym_container")
            with TabPane("lifting"):
                yield LiftingContainer(id="lifting_container")

        yield Footer(id="app_footer")

    def on_mount(self) -> None:
        self.update_gym_container()
        self.update_lifting_container()

    def update_gym_container(self) -> None:
        gc = self.query_one("#gym_container", GymContainer)
        with self.sf.session() as session:
            units = self.load_unit_service.load_gym_units(session)
            gc.set_units(units)

    def update_lifting_container(self) -> None:
        gc = self.query_one("#lifting_container", LiftingContainer)
        with self.sf.session() as session:
            units = self.load_unit_service.load_lifting_units(session)
            gc.set_units(units)

    def action_log_unit(self) -> None:
        # TODO update other widgets after saving a units
        self.push_screen(LogUnitScreen(self.log_unit_service.unit_names, self.log_unit))

    async def log_unit(self, line: str) -> None:
        with self.sf.session() as session:
            self.log_unit_service.log_unit(line, session)
