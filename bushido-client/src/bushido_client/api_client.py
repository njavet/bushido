from typing import TypeVar

from httpx import AsyncClient
from pydantic import BaseModel, TypeAdapter

from bushidolib.unit.base import BaseUnit

TUnit = TypeVar("TUnit", bound=BaseModel)


_unit_adapter: TypeAdapter[BaseUnit] = TypeAdapter(BaseUnit)


class BushidoApiClient:
    def __init__(self, base_url: str) -> None:
        self._client = AsyncClient(base_url=base_url)

    async def get_unit_names(self) -> list[str]:
        response = await self._client.get("/api/unit-names")
        response.raise_for_status()
        return list(response.json())

    async def log_unit(self, line: str) -> BaseUnit:
        response = await self._client.post(
            "/api/unit-logs",
            json={"line": line},
        )
        response.raise_for_status()
        return _unit_adapter.validate_python(response.json())

    async def close(self) -> None:
        await self._client.aclose()
