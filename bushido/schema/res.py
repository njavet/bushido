from datetime import date
from pydantic import BaseModel


class UnitLogResponse(BaseModel):
    date: date
    hms: str
    emoji: str
    payload: str
