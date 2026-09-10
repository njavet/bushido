import datetime
from typing import TypeVar

from httpx import AsyncClient
from pydantic import BaseModel, TypeAdapter

from bushidolib.category.base import BaseUnit
from bushidolib.constants import UnitCategory

TUnit = TypeVar("TUnit", bound=BaseModel)


_unit_adapter: TypeAdapter[BaseUnit] = TypeAdapter(BaseUnit)


class BushidoApiClient:
    def __init__(self, base_url: str) -> None:
        self._client = AsyncClient(base_url=base_url)

    async def log_unit(self, line: str) -> BaseUnit:
        response = await self._client.post(
            "/api/unit-logs",
            json={"line": line},
        )
        response.raise_for_status()
        return _unit_adapter.validate_python(response.json())

    async def load_units(
        self,
        unit_category: UnitCategory,
        unit_type: type[TUnit],
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[TUnit]:
        response = await self._client.post(
            "/api/unit-logs/query",
            json={
                "unit_category": unit_category,
                "start_time": start_t,
                "end_time": end_t,
            },
        )
        response.raise_for_status()
        return [unit_type.model_validate(u) for u in response.json()]

    async def close(self) -> None:
        await self._client.aclose()
