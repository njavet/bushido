import datetime
from typing import Any

from sqlalchemy.orm import Session

from .cardio import CardioUnit
from .dtypes import CategoryRegistration, ParsedUnit, SystemClock, TrainingUnit
from .exceptions import ParsingError
from .gym import GymUnit
from .lifting import LiftingUnit
from .parsing.unit import parse_raw_unit, split_options
from .protocols import Clock
from .registry import REGISTRY, UNIT_TO_CATEGORY, get_category_help
from .wimhof import WimhofUnit


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
        gym_units = self.load_gym_units(session, start_t, end_t)

    def load_wimhof_units(
        self,
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[WimhofUnit]:
        registry = REGISTRY["wimhof"]
        return self._load_units(session, registry, start_t, end_t)

    def load_lifting_units(
        self,
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[LiftingUnit]:
        registry = REGISTRY["lifting"]
        return self._load_units(session, registry, start_t, end_t)

    def load_cardio_units(
        self,
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[CardioUnit]:
        registry = REGISTRY["cardio"]
        return self._load_units(session, registry, start_t, end_t)

    def load_gym_units(
        self,
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[GymUnit]:
        registry = REGISTRY["gym"]
        return self._load_units(session, registry, start_t, end_t)

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
