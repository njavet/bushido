from containers import HeaderContainer, LiftingContainer
from .containers.gym import GymContainer
from .containers.spartan import SpartanContainer
from .screens.log_unit import LogUnitScreen
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)


class BushidoApp(App[None]):
    CSS_PATH = "main.tcss"
    BINDINGS = [
        Binding("q", "quit", "quit"),
        Binding("l", "log_unit", "log"),
        Binding("escape", "cancel", "cancel"),
    ]

    def compose(self) -> ComposeResult:
        yield HeaderContainer()
        yield Rule(line_style="dashed")
        with TabbedContent(id="main_tabs"):
            with TabPane("spartan"):
                yield SpartanContainer(id="spartan_container")
            with TabPane("gym"):
                yield GymContainer(id="gym_container")
            with TabPane("lifting"):
                yield LiftingContainer(id="lifting_container")

        yield Footer(id="app_footer")

