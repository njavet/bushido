import datetime
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Protocol, TypeVar

from sqlalchemy.orm import Session

from bushido.domain.units import Unit

T_DOMAIN = TypeVar("T_DOMAIN")
R_DOMAIN = TypeVar("R_DOMAIN", covariant=True)


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...


@dataclass(frozen=True, slots=True)
class SystemClock:
    timezone: datetime.tzinfo = datetime.UTC

    def now(self) -> datetime.datetime:
        return datetime.datetime.now(self.timezone)


@dataclass(frozen=True, slots=True)
class UnitRegistration:
    parser: UnitParser[Any]
    repo_factory: Callable[[Session], UnitRepo[Any]]
    grammar: str
    emoji: str

    def repo(self, session: Session) -> UnitRepo[Any]:
        return self.repo_factory(session)


class UnitMetric(Protocol[T_DOMAIN, R_DOMAIN]):
    def compute(self, units: Iterable[Unit[T_DOMAIN]]) -> R_DOMAIN: ...


class UnitRepo(Protocol[T_DOMAIN]):
    def add_unit(self, unit: Unit[T_DOMAIN]) -> None: ...
    def fetch_units(
        self,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[T_DOMAIN]]: ...


class UnitParser(Protocol[R_DOMAIN]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> R_DOMAIN: ...
