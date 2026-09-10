import datetime
from typing import Literal

from pydantic import BaseModel

from bushidolib.constants import UnitCategory


class GymData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = None
    focus: str | None = None
