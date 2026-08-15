import datetime
from typing import Literal

from pydantic import BaseModel

from bushidolib.constants import UnitCategory
from bushidolib.unit import BaseUnit

grammar = """
<name> <start> <sec> <loc> [<dist>] [<avg_hr>] [<max_hr>] [<cal>] # [<comment>]
    """


class CardioData(BaseModel):
    start_t: datetime.time
    seconds: float
    location: str
    distance: float | None
    avg_hr: int | None
    max_hr: int | None
    calories: int | None


class CardioUnit(BaseUnit):
    unit_category: Literal[UnitCategory.CARDIO] = UnitCategory.CARDIO
    data: CardioData
