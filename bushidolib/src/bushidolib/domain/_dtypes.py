import datetime
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol, TypeVar

T_DOMAIN = TypeVar("T_DOMAIN")
R_DOMAIN_co = TypeVar("R_DOMAIN_co", covariant=True)


class UnitMetric(Protocol[T_DOMAIN, R_DOMAIN_co]):
    def compute(self, units: Iterable[Unit[T_DOMAIN]]) -> R_DOMAIN_co: ...


@dataclass(frozen=True, slots=True)
class Unit[T]:
    name: str
    log_time: datetime.datetime
    comment: str | None
    data: T
