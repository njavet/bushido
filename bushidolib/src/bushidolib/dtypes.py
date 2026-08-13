from collections.abc import Iterable
from typing import Protocol, TypeVar

from bushidolib.units import Unit

T_DOMAIN = TypeVar("T_DOMAIN")
R_DOMAIN = TypeVar("R_DOMAIN", covariant=True)


class UnitMetric(Protocol[T_DOMAIN, R_DOMAIN]):
    def compute(self, units: Iterable[Unit[T_DOMAIN]]) -> R_DOMAIN: ...


class UnitParser(Protocol[R_DOMAIN]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> R_DOMAIN: ...
