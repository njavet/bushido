from collections.abc import Iterable
from typing import Protocol, TypeVar

from bushidolib.domain import Unit

T_DOMAIN = TypeVar("T_DOMAIN")
R_DOMAIN_co = TypeVar("R_DOMAIN_co", covariant=True)


class UnitMetric(Protocol[T_DOMAIN, R_DOMAIN_co]):
    def compute(self, units: Iterable[Unit[T_DOMAIN]]) -> R_DOMAIN_co: ...
