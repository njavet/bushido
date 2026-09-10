import datetime
from typing import Literal, dataclass_transform

from pydantic import BaseModel

from bushidolib.constants import UnitCategory



class CardioData(BaseModel):
    start_t: datetime.time
    seconds: float
    gym: str
    distance: float | None = None
    avg_hr: int | None = None
    max_hr: int | None = None
    calories: int | None = None
