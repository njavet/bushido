from httpx import AsyncClient, Response

from bushidolib.constants import UnitCategory
from bushidolib.contracts.log_res import UnitLogResponse
from bushidolib.contracts.req import LoadUnitRequest, LogUnitRequest
from bushidolib.contracts.unit import (
    CardioUnit,
    GymUnit,
    LiftingUnit,
    UnitSetting,
    WimhofUnit,
)


class BushidoApiClient:
    def __init__(self, base_url: str) -> None:
        self._client = AsyncClient(base_url=base_url)

    async def load_unit_settings(self) -> dict[str, UnitCategory]:
        response = await self._client.get("/api/unit-settings")
        response.raise_for_status()
        unit_settings = [UnitSetting.model_validate(s) for s in response.json()]
        return {setting.name: setting.category for setting in unit_settings}

    async def log_unit(self, request: LogUnitRequest) -> UnitLogResponse:
        response = await self._client.post(
            "/api/unit-logs",
            json=request.model_dump(mode="json"),
        )
        response.raise_for_status()
        return UnitLogResponse.model_validate(response.json())

    async def load_cardio_units(self, request: LoadUnitRequest) -> list[CardioUnit]:
        response = await self._load_units(request)
        return [CardioUnit.model_validate(u) for u in response.json()]

    async def load_gym_units(self, request: LoadUnitRequest) -> list[GymUnit]:
        response = await self._load_units(request)
        return [GymUnit.model_validate(u) for u in response.json()]

    async def load_lifting_units(self, request: LoadUnitRequest) -> list[LiftingUnit]:
        response = await self._load_units(request)
        return [LiftingUnit.model_validate(u) for u in response.json()]

    async def load_wimhof_units(self, request: LoadUnitRequest) -> list[WimhofUnit]:
        response = await self._load_units(request)
        return [WimhofUnit.model_validate(u) for u in response.json()]

    async def _load_units(self, request: LoadUnitRequest) -> Response:
        response = await self._client.post(
            "/api/unit-logs/query", json=request.model_dump(mode="json")
        )
        response.raise_for_status()
        return response

    async def close(self) -> None:
        await self._client.aclose()
