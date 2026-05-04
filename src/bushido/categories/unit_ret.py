import datetime
from typing import Any

from sqlalchemy.orm import Session

from .registry import REGISTRY


class UnitLoadService:
    def load_units(
        self,
        session: Session,
        category: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> Any:
        total = []
        for category, registration in REGISTRY.items():
            units = registration.repo(session).fetch_units(start_t=start_t, end_t=end_t)
            for unit in units:
                print("NAME", unit.name)
            total += units
        return total
