import datetime
from abc import ABC
from typing import Generic, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption

from bushido.db.db_model import UnitTable

T = TypeVar("T", bound=UnitTable)


class UnitRepo(ABC, Generic[T]):
    def __init__(
        self,
        session: Session,
        unit_cls: type[T],
    ) -> None:
        self.session = session
        self.unit_cls = unit_cls

    def add_unit(self, unit: T) -> None:
        self.session.add(unit)
        self.session.commit()

    def fetch_units(
        self,
        unit_name: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[T]:
        return self._fetch_units(unit_name, start_t, end_t)

    def _fetch_units(
        self,
        unit_name: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
        options: Sequence[ORMOption] = (),
    ) -> list[T]:
        stmt = select(self.unit_cls).options(*options)
        if unit_name is not None:
            stmt = stmt.where(self.unit_cls.name == unit_name)
        if start_t is not None:
            stmt = stmt.where(start_t <= self.unit_cls.log_time)
        if end_t is not None:
            stmt = stmt.where(self.unit_cls.log_time <= end_t)
        stmt = stmt.order_by(self.unit_cls.log_time.desc())
        return list(self.session.scalars(stmt))
