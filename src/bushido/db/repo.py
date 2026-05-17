import datetime
from typing import Generic, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption

from .model.base import UnitTable

T_ORM = TypeVar("T_ORM", bound=UnitTable)


class UnitRepo(Generic[T_ORM]):
    def __init__(
        self,
        session: Session,
        unit_cls: type[T_ORM],
        load_options: Sequence[ORMOption] = (),
    ) -> None:
        self.session = session
        self.unit_cls = unit_cls
        self.load_options = load_options

    def add_unit(self, unit: T_ORM) -> None:
        self.session.add(unit)
        self.session.commit()

    def fetch_units(
        self,
        unit_name: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> Sequence[T_ORM]:
        stmt = select(self.unit_cls).options(*self.load_options)
        if unit_name is not None:
            stmt = stmt.where(self.unit_cls.name == unit_name)
        if start_t is not None:
            stmt = stmt.where(start_t <= self.unit_cls.log_time)
        if end_t is not None:
            stmt = stmt.where(self.unit_cls.log_time <= end_t)
        stmt = stmt.order_by(self.unit_cls.log_time.desc())
        return list(self.session.scalars(stmt))
