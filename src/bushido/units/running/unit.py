import datetime
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RunningData:
    start_t: datetime.time
    seconds: float
    location: str
    distance: float | None
    avg_hr: int | None
    max_hr: int | None
    calories: int | None
