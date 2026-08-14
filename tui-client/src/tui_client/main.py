import asyncio
from typing import ClassVar, override

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from tui_client.api_client import BushidoApiClient
from tui_client.screens import LogUnitScreen
from tui_client.settings import UnitConf, unit_emojis

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

    def __init__(
        self, api_client: BushidoApiClient, unit_settings: dict[str, UnitConf]
    ) -> None:
        super().__init__()
        # TODO investigate defaults ({}, [])
        self.api = api_client
        self.unit_settings = unit_settings

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
                yield LiftingContainer(unit_settings=self.unit_settings)

        yield Footer(id="app_footer")

    async def action_log_unit(self) -> None:
        await self.push_screen(LogUnitScreen(self.api, list(self.unit_settings.keys())))

    async def on_unmount(self) -> None:
        await self.api.close()


async def async_main() -> None:
    api_client = BushidoApiClient(base_url="http://localhost:8000")
    settings = await api_client.load_unit_settings()
    unit_settings = {
        s.name: UnitConf(emoji=unit_emojis[s.name], category=s.category)
        for s in settings
    }
    app = BushidoApp(api_client=api_client, unit_settings=unit_settings)
    await app.run_async()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
