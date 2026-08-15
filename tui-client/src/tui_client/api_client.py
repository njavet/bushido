import datetime
from typing import TypeVar, Annotated

from httpx import AsyncClient
from pydantic import BaseModel, Field, TypeAdapter

from bushidolib.cardio import CardioUnit
from bushidolib.constants import UnitCategory
from bushidolib.gym import GymUnit
from bushidolib.lifting import LiftingUnit
from bushidolib.unit import UnitSetting
from bushidolib.wimhof import WimhofUnit

TUnit = TypeVar("TUnit", bound=BaseModel)


LoggedUnit = Annotated[
    CardioUnit | GymUnit | LiftingUnit | WimhofUnit,
    Field(discriminator="unit_category"),
]
_unit_adapter = TypeAdapter(LoggedUnit)


class BushidoApiClient:
    def __init__(self, base_url: str) -> None:
        self._client = AsyncClient(base_url=base_url)

    async def load_unit_settings(self) -> list[UnitSetting]:
        response = await self._client.get("/api/unit-settings")
        response.raise_for_status()
        return [UnitSetting.model_validate(s) for s in response.json()]

    async def log_unit(self, line: str) -> LoggedUnit:
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
