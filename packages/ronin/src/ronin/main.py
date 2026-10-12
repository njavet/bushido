import asyncio
from typing import ClassVar, override

import httpx
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from ronin.dtypes import UnitLogResult
from ronin.settings import BASE_URL, unit_emojis
from sekkin.api_client import BushidoApiClient

from .containers import (
    CardioContainer,
    HeaderContainer,
    LogsContainer,
    MartialArtsContainer,
    ProfileContainer,
    StrengthContainer,
    WorkContainer,
)


class BushidoApp(App[None]):
    CSS_PATH = "assets/static/main.tcss"
    BINDINGS: ClassVar = [
        Binding("q", "quit", "quit"),
        Binding("l", "log_unit", "log"),
    ]

    def __init__(self, api_client: BushidoApiClient, unit_names: list[str]) -> None:
        super().__init__()
        self.api = api_client
        self.unit_names = unit_names

    @override
    def compose(self) -> ComposeResult:
        yield HeaderContainer()
        yield Rule(line_style="dashed")
        with TabbedContent(id="main_tabs"):
            with TabPane("profile"):
                yield ProfileContainer()
            with TabPane("martial_arts"):
                yield MartialArtsContainer(unit_emojis)
            with TabPane("strength"):
                yield StrengthContainer(unit_emojis)
            with TabPane("cardio"):
                yield CardioContainer()
            with TabPane("work"):
                yield WorkContainer()
            with TabPane("logs"):
                yield LogsContainer()
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

    def on_log_unit_closed(self, result: UnitLogResult | None) -> None:
        if result is None or result.unit is None:
            return

    async def on_unmount(self) -> None:
        await self.api.close()


async def async_main() -> None:
    api_client = BushidoApiClient(base_url=BASE_URL)
    try:
        unit_names = await api_client.get_unit_names()
    except httpx.ConnectError:
        print("Failed to connect to the server. Is it running?")
        await api_client.close()
        return

    try:
        app = BushidoApp(api_client=api_client, unit_names=unit_names)
        await app.run_async()
    finally:
        await api_client.close()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
