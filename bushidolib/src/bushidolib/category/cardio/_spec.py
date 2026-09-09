import datetime
from typing import Literal

from pydantic import BaseModel

from bushidolib.constants import UnitCategory


class CardioData(BaseModel):
    unit_category: Literal[UnitCategory.CARDIO] = UnitCategory.CARDIO
    start_t: datetime.time
    seconds: float
    gym: str
    distance: float | None = None
    avg_hr: int | None = None
    max_hr: int | None = None
    calories: int | None = None
