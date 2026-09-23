import asyncio
from typing import ClassVar, override

import httpx
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from bushido_client.api_client import BushidoApiClient
from bushidolib.unit.martial_arts import MartialArtsUnit
from bushidolib.unit.strength import LiftingUnit
from tui_client.dtypes import UnitLogResult
from tui_client.screens import LogUnitScreen
from tui_client.settings import unit_emojis

from .containers import (
    GymContainer,
    HeaderContainer,
    LiftingContainer,
    SpartanContainer,
)


def filter_units(
    unit_settings: dict[str, str], units: list[str],
) -> dict[str, str]:
    return {
        name: emoji
        for name, emoji in unit_settings.items()
        if name in units
    }


class BushidoApp(App[None]):
    CSS_PATH = "assets/static/main.tcss"
    BINDINGS: ClassVar = [
        Binding("q", "quit", "quit"),
        Binding("l", "log_unit", "log"),
    ]

    def __init__(
        self, api_client: BushidoApiClient
    ) -> None:
        super().__init__()
        self.api = api_client

    @override
    def compose(self) -> ComposeResult:
        yield HeaderContainer()
        yield Rule(line_style="dashed")
        with TabbedContent(id="main_tabs"):
            with TabPane("spartan"):
                yield SpartanContainer(id="spartan_container")
            with TabPane("martial_arts"):
                yield GymContainer(filter_units(unit_emojis, ['strength']))
            with TabPane("strength"):
                yield LiftingContainer(
                    unit_settings=filter_units(unit_emojis, ["squats"])
                )
        yield Footer(id="app_footer")

    """
    async def on_mount(self) -> None:
        self.load_lifting_units()
        self.load_gym_units()

    @work
    async def load_lifting_units(self) -> None:
        units = await self.api.load_units(UnitCategory.LIFTING, LiftingUnit)
        self.query_one(LiftingContainer).set_units(units)

    @work
    async def load_gym_units(self) -> None:
        units = await self.api.load_units(UnitCategory.GYM, GymUnit)
        self.query_one(GymContainer).set_units(units)
    """

    async def action_log_unit(self) -> None:
        await self.push_screen(
            LogUnitScreen(self.api, list(unit_emojis.keys())),
            callback=self.on_log_unit_closed,
        )

    def on_log_unit_closed(self, result: UnitLogResult | None) -> None:
        if result is None or result.unit is None:
            return
        match result.unit:
            case LiftingUnit():
                self.query_one(LiftingContainer).add_unit(result.unit)

    async def on_unmount(self) -> None:
        await self.api.close()


async def async_main() -> None:
    api_client = BushidoApiClient(base_url="http://localhost:8000")
    try:
        settings = [{"name": "yo", "category": "yo"}]
    except httpx.ConnectError:
        print("Failed to connect to the server. Is it running?")
        await api_client.close()
        return

    try:
        app = BushidoApp(api_client=api_client)
        await app.run_async()
    finally:
        await api_client.close()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
