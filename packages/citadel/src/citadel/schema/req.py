import datetime

from pydantic import BaseModel, Field


class LogUnitRequest(BaseModel):
    line: str = Field(min_length=1)


class LoadUnitRequest(BaseModel):
    unit_name: str
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None
