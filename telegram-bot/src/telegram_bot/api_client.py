from httpx import AsyncClient

from bushidolib.contracts.unit import (
    UnitSetting,
)


class BushidoApiClient:
    def __init__(self, base_url: str) -> None:
        self._client = AsyncClient(base_url=base_url)

    async def load_unit_settings(self) -> list[UnitSetting]:
        response = await self._client.get("/api/unit-settings")
        response.raise_for_status()
        return [UnitSetting.model_validate(s) for s in response.json()]

    async def log_unit(self, line: str) -> str:
        response = await self._client.post(
            "/api/unit-logs",
            json={"line": line},
        )
        response.raise_for_status()
        return str(response.json()["status"])

    async def close(self) -> None:
        await self._client.aclose()
