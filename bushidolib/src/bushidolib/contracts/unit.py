from enum import StrEnum

from pydantic import BaseModel




class UnitCategory(StrEnum):
    CARDIO = "cardio"
    GYM = "gym"
    LIFTING = "lifting"
    WIMHOF = "wimhof"


class UnitSetting(BaseModel):
    name: str
    category: UnitCategory
