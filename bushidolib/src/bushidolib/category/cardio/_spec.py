import datetime

from pydantic import BaseModel

from bushidolib.schema.unit import BaseUnit


class CardioData(BaseModel):
    start_t: datetime.time
    seconds: float
    gym: str
    distance: float | None = None
    avg_hr: int | None = None
    max_hr: int | None = None
    calories: int | None = None


class CardioUnit(BaseUnit, CardioData):
    pass
