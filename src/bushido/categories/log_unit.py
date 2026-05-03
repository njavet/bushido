from sqlalchemy.orm import Session

from .dtypes import CategoryHelp, Clock, ParsedUnit, SystemClock
from .exceptions import ParsingError
from .parsing.unit import parse_raw_unit, split_options
from .registry import REGISTRY, UNIT_TO_CATEGORY, get_unit_names


class LogUnitService:
    def __init__(self, clock: Clock = SystemClock()) -> None:
        self.clock = clock
        self.registry = REGISTRY

    def log_unit(self, line: str, session: Session) -> str | None:
        try:
            raw = parse_raw_unit(line)
        except ParsingError as e:
            return str(e)
        try:
            category = UNIT_TO_CATEGORY[raw.name]
        except KeyError:
            return f"unknown unit: {raw.name}"

        registry = self.registry[category]
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

    @property
    def unit_names(self) -> list[str]:
        return get_unit_names()

    @property
    def category_help(self) -> list[CategoryHelp]:
        return [
            CategoryHelp(name=category, grammar=r.grammar, unit_names=r.unit_names)
            for category, r in REGISTRY.items()
        ]
