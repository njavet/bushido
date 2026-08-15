import datetime

from pydantic import BaseModel

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
    data: CardioData
