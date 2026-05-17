import datetime
from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption

from bushido.dtypes import T_DOMAIN, Unit

from ..models import UnitTable

T_ORM = TypeVar("T_ORM", bound=UnitTable)


class BaseUnitRepo(ABC, Generic[T_DOMAIN, T_ORM]):
    orm_cls: type[T_ORM]
    load_options: Sequence[ORMOption] = ()

    def __init__(self, session: Session) -> None:
        self.session = session

    def add_unit(self, unit: Unit[T_DOMAIN]) -> None:
        self.session.add(self._to_orm(unit))
        self.session.commit()

    def fetch_units(
        self,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[T_DOMAIN]]:
        stmt = select(self.orm_cls).options(*self.load_options)
        if start_t is not None:
            stmt = stmt.where(start_t <= self.orm_cls.log_time)
        if end_t is not None:
            stmt = stmt.where(self.orm_cls.log_time <= end_t)
        stmt = stmt.order_by(self.orm_cls.log_time.desc())
        return [self._from_orm(unit) for unit in self.session.scalars(stmt)]

    @staticmethod
    @abstractmethod
    def _to_orm(unit: Unit[T_DOMAIN]) -> T_ORM: ...

    @staticmethod
    @abstractmethod
    def _from_orm(orm_unit: T_ORM) -> Unit[T_DOMAIN]: ...
