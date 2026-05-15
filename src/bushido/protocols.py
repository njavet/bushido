import datetime
from typing import Protocol, TypeVar


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...
