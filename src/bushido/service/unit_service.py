import datetime
from typing import Any

from sqlalchemy.orm import Session

from bushido.unit import LiftingUnit
from bushido.unit.dtypes import (
    CategoryRegistration,
    ParsedUnit,
    SystemClock,
    TrainingUnit,
)
from bushido.unit.gym.unit import compute_duration
from bushido.unit.registry import REGISTRY, UNIT_TO_CATEGORY, get_category_help
from bushido.core.exceptions import ParsingError
from bushido.core.parsing.unit import parse_raw_unit, split_options
from bushido.unit.protocols import Clock


class UnitService:
    def __init__(self, clock: Clock = SystemClock()) -> None:
        self.clock = clock
        self.unit_names = sorted(UNIT_TO_CATEGORY)
        self.category_help = get_category_help()

    def log_unit(self, line: str, session: Session) -> str | None:
        try:
            raw = parse_raw_unit(line)
        except ParsingError as e:
            return str(e)
        try:
            category = UNIT_TO_CATEGORY[raw.name]
        except KeyError:
            return f"unknown unit: {raw.name}"

        registry = REGISTRY[category]
        tokens, log_time = split_options(raw.tokens, self.clock)
        try:
            unit_data = registry.parser.parse(tokens)
        except ParsingError as e:
            return str(e)

        parsed_unit = ParsedUnit(
            name=raw.name,
            emoji=registry.unit_settings[raw.name],
            data=unit_data,
            log_time=log_time,
            comment=raw.comment,
        )
        unit = registry.mapper.to_orm(parsed_unit)
        registry.repo(session).add_unit(unit)
        return None

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
