from datetime import date
from pydantic import BaseModel


class MDResponse(BaseModel):
    categories: dict[str, list[tuple[str, str]]]


class UnitResponse(BaseModel):
    date: date
    hms: str
    emoji: str
    unit_name: str
    payload: str
