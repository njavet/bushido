import datetime
from dataclasses import dataclass
from typing import TypeVar

T_DOMAIN = TypeVar("T_DOMAIN")
R_DOMAIN_co = TypeVar("R_DOMAIN_co", covariant=True)


@dataclass(frozen=True, slots=True)
class Unit[T]:
    name: str
    log_time: datetime.datetime
    comment: str | None
    data: T
