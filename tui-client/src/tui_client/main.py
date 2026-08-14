from typing import ClassVar, override

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from bushidolib.constants import UnitCategory
from tui_client.api_client import BushidoApiClient
from tui_client.screens import LogUnitScreen

from .containers import HeaderContainer, LiftingContainer
from .containers.gym import GymContainer
from .containers.spartan import SpartanContainer


class BushidoApp(App[None]):
    CSS_PATH = "main.tcss"
    BINDINGS: ClassVar = [
        Binding("q", "quit", "quit"),
        Binding("l", "log_unit", "log"),
        Binding("escape", "cancel", "cancel"),
    ]

    def __init__(self) -> None:
        super().__init__()
        # TODO investigate defaults ({}, [])
        self.unit_settings: dict[str, UnitCategory] = {}
        self.api = BushidoApiClient(base_url="http://localhost:8000")

    @override
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

    async def on_mount(self) -> None:
        self.unit_settings = await self.api.load_unit_settings()

    async def action_log_unit(self) -> None:
        await self.push_screen(LogUnitScreen(self.api, list(self.unit_settings.keys())))

    async def on_unmount(self) -> None:
        await self.api.close()


def main() -> None:
    BushidoApp().run()


if __name__ == "__main__":
    main()
