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


class UnitLogService:
    def __init__(self, clock: Clock = SystemClock()) -> None:
        self.clock = clock

    def log_unit(self, line: str, session: Session) -> None:
        raw = parse_raw_unit(line)

        category = UNIT_TO_CATEGORY[raw.name]
        tokens, log_time_str = split_options(raw.tokens)
        if log_time_str:
            log_time = parse_datetime(log_time_str)
        else:
            log_time = self.clock.now()

        registry = REGISTRY[category]
        unit_data = registry.parser.parse(tokens)

        parsed_unit = ParsedUnit(
            name=raw.name,
            emoji=registry.unit_settings[raw.name],
            data=unit_data,
            log_time=log_time,
            comment=raw.comment,
        )
        unit = registry.mapper.to_orm(parsed_unit)
        registry.repo(session).add_unit(unit)


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


def parse_raw_unit(line: str) -> RawUnit:
    body, sep, comment = line.partition("#")
    tokens = tuple(body.split())

    if not tokens:
        raise ParsingError(f"Empty unit line: {line}")

    return RawUnit(
        name=tokens[0],
        tokens=tokens[1:],
        comment=comment.strip() if sep and comment.strip() else None,
    )


def split_options(tokens: tuple[str, ...]) -> tuple[tuple[str, ...], str | None]:
    clean: list[str] = []
    log_time: str | None = None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "--dt":
            if i + 1 >= len(tokens):
                raise ParsingError("--dt requires a value")
            log_time = tokens[i + 1]
            i += 2
            continue
        clean.append(token)
        i += 1
    return tuple(clean), log_time

