from httpx import AsyncClient

from bushidolib.contracts.log_req import LogUnitRequest
from bushidolib.contracts.log_res import UnitLogResponse


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
