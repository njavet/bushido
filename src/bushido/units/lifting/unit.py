import datetime
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LiftingData:
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = None
    focus: str | None = None


def compute_duration(start_t: datetime.time, end_t: datetime.time) -> int:
    return (
        datetime.datetime.combine(datetime.date.today(), end_t)
        - datetime.datetime.combine(datetime.date.today(), start_t)
    ).seconds // 60
