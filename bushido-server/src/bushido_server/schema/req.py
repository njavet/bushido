from pydantic import BaseModel, Field


class LogUnitRequest(BaseModel):
    line: str = Field(min_length=1)
