import datetime
from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True, slots=True)
class Unit(ABC):
    name: str
    emoji: str
    log_time: datetime.datetime
    comment: str | None
