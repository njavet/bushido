import asyncio
from typing import ClassVar, override

import httpx
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Rule

from ronin.settings import BASE_URL
from ronin.widgets.command_line import CommandLine
from sekkin.api_client import BushidoApiClient

from .containers import HeaderContainer


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
        yield CommandLine(commands=self.unit_names)
        yield Footer(id="app_footer")

    async def on_unmount(self) -> None:
        await self.api.close()


"""
    async def on_command_submitted(self, message: CommandSubmitted) -> None:
        if not message.value:
            self.notify(
                "empty domain",
                title="logging failed",
                severity="error",
            )
            return

        try:
            unit = await self.api.log_unit(line=message.value)
        except Exception as exc:
            self.notify(
                str(exc),
                title="logging failed",
                severity="error",
            )
            return

        self.notify(
            f"logged unit: {message.value.split()[0]}",
            title="logging successful",
            severity="information",
        )
"""


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
