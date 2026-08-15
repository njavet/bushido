import datetime

from pydantic import BaseModel, Field

from bushidolib.constants import UnitCategory


class LogUnitRequest(BaseModel):
    line: str = Field(min_length=1)


class LoadUnitRequest(BaseModel):
    unit_category: UnitCategory
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None
