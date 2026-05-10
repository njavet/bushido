import datetime

from sqlalchemy.orm import Session

from .cardio import CardioUnit
from .dtypes import Clock, ParsedUnit, SystemClock
from .exceptions import ParsingError
from .gym import GymUnit
from .lifting import LiftingUnit
from .parsing.unit import parse_raw_unit, split_options
from .registry import REGISTRY, UNIT_TO_CATEGORY, get_category_help
from .unit_settings import DEFAULT_CATEGORIES
from .wimhof import WimhofUnit

type AnyUnit = GymUnit | CardioUnit | LiftingUnit | WimhofUnit


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
        if not registry.repo(session).add_unit(unit):
            return "repo error"
        else:
            return None

    def load_units(
        self,
        session: Session,
        categories: tuple[str, ...] = DEFAULT_CATEGORIES,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> dict[str, list[AnyUnit]]:
        result = {}
        for category in categories:
            result[category] = self._load_units(session, category, start_t, end_t)
        return result

    @staticmethod
    def load_gym_units(
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[GymUnit]:
        registry = REGISTRY["gym"]
        units = registry.repo(session).fetch_units(start_t=start_t, end_t=end_t)
        parsed_units = [registry.mapper.from_orm(unit) for unit in units]
        return parsed_units

    @staticmethod
    def _load_units(
        session: Session,
        category: str,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[AnyUnit]:
        registry = REGISTRY[category]
        units = registry.repo(session).fetch_units(start_t=start_t, end_t=end_t)
        parsed_units = [registry.mapper.from_orm(unit) for unit in units]
        return parsed_units
