import datetime
from dataclasses import dataclass
from typing import Protocol

from tui_client.settings import LOCAL_TIMEZONE


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...


@dataclass(frozen=True, slots=True)
class SystemClock:
    timezone: datetime.tzinfo = LOCAL_TIMEZONE

    def now(self) -> datetime.datetime:
        return datetime.datetime.now(self.timezone)
