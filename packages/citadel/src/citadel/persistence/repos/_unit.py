import datetime
from abc import ABC, abstractmethod
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption

from citadel.domain.unit import BaseUnit

from ..models import UnitTable


class UnitRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def count(self, spartan_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(UnitTable)
            .where(UnitTable.spartan_id == spartan_id)
        )
        return self.session.scalar(stmt) or 0

    def fetch_units(
        self,
        spartan_id: int,
        limit: int = 101,
    ) -> list[UnitTable]:
        stmt = (
            select(UnitTable)
            .where(UnitTable.spartan_id == spartan_id)
            .order_by(UnitTable.log_time.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt))
