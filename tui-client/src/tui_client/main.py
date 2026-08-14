from typing import ClassVar, override

from httpx import AsyncClient
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Footer,
    Rule,
    TabbedContent,
    TabPane,
)

from bushidolib.contracts.log_req import LogUnitRequest
from bushidolib.contracts.log_res import UnitLogResponse

from .containers import HeaderContainer, LiftingContainer
from .containers.gym import GymContainer
from .containers.spartan import SpartanContainer


class BushidoApiClient:
    def __init__(self, base_url: str) -> None:
        self._client = AsyncClient(base_url=base_url)

    async def log_unit(self, request: LogUnitRequest) -> UnitLogResponse:
        response = await self._client.post(
            "/unit-logs",
            json=request.model_dump(mode="json"),
        )
        response.raise_for_status()
        return UnitLogResponse.model_validate(response.json())

    async def close(self) -> None:
        await self._client.aclose()


class BushidoApp(App[None]):
    CSS_PATH = "main.tcss"
    BINDINGS: ClassVar = [
        Binding("q", "quit", "quit"),
        Binding("l", "log_unit", "log"),
        Binding("escape", "cancel", "cancel"),
    ]

    def __init__(self) -> None:
        super().__init__()
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


def main() -> None:
    BushidoApp().run()


if __name__ == "__main__":
    main()
