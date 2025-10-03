import datetime
from dataclasses import dataclass


@dataclass
class GymSpec:
    start_t: datetime.time
    end_t: datetime.time
    location: str
    training: str | None = None
    focus: str | None = None
