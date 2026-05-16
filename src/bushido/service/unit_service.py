import datetime
from typing import Any

from sqlalchemy.orm import Session

from bushido.unit.base import RawUnit
from bushido.unit.dt_parse import parse_datetime
from bushido.unit.exceptions import ParsingError
from bushido.dtypes import (
    ParsedUnit,
    SystemClock,
    TrainingUnit,
)
from bushido.protocols import Clock
from bushido.schema.req import LogRequest


class UnitService:
    def __init__(self, clock: Clock = SystemClock()) -> None:
        self.clock = clock

    def load_training_units(
        self,
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[TrainingUnit]:
        result = []
        for unit in self._load_units(session, REGISTRY["gym"], start_t, end_t):
            result.append(
                TrainingUnit(
                    name=unit.name,
                    emoji=unit.emoji,
                    date=unit.log_time.date(),
                    duration=compute_duration(unit.data.start_t, unit.data.end_t),
                    start_t=unit.data.start_t,
                    end_t=unit.data.end_t,
                    gym=unit.data.gym,
                    comment=unit.comment,
                )
            )
        for unit in self._load_units(session, REGISTRY["cardio"], start_t, end_t):
            result.append(
                TrainingUnit(
                    name=unit.name,
                    emoji=unit.emoji,
                    date=unit.log_time.date(),
                    duration=int(unit.data.seconds / 60),
                    start_t=unit.data.start_t,
                    gym=unit.data.location,
                    comment=unit.comment,
                )
            )
        return sorted(result, key=lambda u: u.date, reverse=True)

    def load_lifting_units(
        self,
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[LiftingUnit]:
        return self._load_units(session, REGISTRY["barbell"], start_t, end_t)

    @staticmethod
    def _load_units(
        session: Session,
        registry: CategoryRegistration,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Any]:
        units = registry.repo(session).fetch_units(start_t=start_t, end_t=end_t)
        parsed_units = [registry.mapper.from_orm(unit) for unit in units]
        return parsed_units

