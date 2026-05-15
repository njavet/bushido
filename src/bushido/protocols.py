import datetime
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...
