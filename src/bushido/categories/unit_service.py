import datetime

from sqlalchemy.orm import Session

from .dtypes import Clock, ParsedUnit, SystemClock
from .exceptions import ParsingError
from .parsing.unit import parse_raw_unit, split_options
from .registry import REGISTRY, UNIT_TO_CATEGORY, get_category_help, get_unit_names


class UnitService:
    def __init__(self, clock: Clock = SystemClock()) -> None:
        self.clock = clock
        self.unit_names = get_unit_names()
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
            data=unit_data,
            log_time=log_time,
            comment=raw.comment,
        )
        unit, subunits = registry.mapper.to_orm(parsed_unit)
        if not registry.repo(session).add_unit(unit, subunits):
            return "repo error"
        else:
            return None

    def load_units(
        self,
        session: Session,
        category: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> None:
        return
