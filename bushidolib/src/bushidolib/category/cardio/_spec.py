import datetime

from ..base import BaseUnit


class CardioUnit(BaseUnit):
    start_t: datetime.time
    seconds: float
    gym: str
    distance: float | None = None
    avg_hr: int | None = None
    max_hr: int | None = None
    calories: int | None = None
