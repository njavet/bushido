import datetime
from typing import Literal

from pydantic import BaseModel

from citadel.exceptions import UnitParsingError
from citadel.unit._base import BaseUnit, RawUnit, UnitType
from citadel.unit.parsing import (
    parse_military_time_string,
    time_string_to_seconds,
)


class CardioData(BaseModel):
    start_t: datetime.time
    seconds: float
    gym: str
    avg_hr: int | None = None
    max_hr: int | None = None
    calories: int | None = None


class RunningUnit(BaseUnit, CardioData):
    unit_type: Literal[UnitType.running] = UnitType.running
    distance: float


class SwimmingUnit(BaseUnit, CardioData):
    unit_type: Literal[UnitType.swimming] = UnitType.swimming
    distance: float
    pool_length: int | None = None
    temperature: float | None = None


class RopeSkipUnit(BaseUnit, CardioData):
    unit_type: Literal[UnitType.skipping] = UnitType.skipping


def parse_cardio_data(tokens: tuple[str, ...], options: dict[str, str]) -> CardioData:
    start_t = parse_military_time_string(tokens[0])
    seconds = time_string_to_seconds(tokens[1])
    try:
        gym = tokens[2]
    except IndexError as e:
        raise UnitParsingError("no gym") from e
    try:
        avg_hr = int(options["avg_hr"])
    except KeyError:
        avg_hr = None
    try:
        max_hr = int(options["max_hr"])
    except KeyError:
        max_hr = None
    try:
        calories = int(options["cal"])
    except KeyError:
        calories = None
    return CardioData(
        start_t=start_t,
        seconds=seconds,
        gym=gym,
        avg_hr=avg_hr,
        max_hr=max_hr,
        calories=calories,
    )


def build_running_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> RunningUnit:
    data = parse_cardio_data(raw_unit.tokens, raw_unit.options)
    try:
        distance = float(raw_unit.tokens[3])
    except (KeyError, ValueError) as e:
        raise UnitParsingError(f"wrong distance {raw_unit.tokens}") from e
    return RunningUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=data.start_t,
        seconds=data.seconds,
        gym=data.gym,
        distance=distance,
        avg_hr=data.avg_hr,
        max_hr=data.max_hr,
        calories=data.calories,
    )


def build_swimming_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> SwimmingUnit:
    data = parse_cardio_data(raw_unit.tokens, raw_unit.options)
    try:
        distance = float(raw_unit.tokens[3])
    except (KeyError, ValueError) as e:
        raise UnitParsingError(f"wrong distance {raw_unit.tokens}") from e
    try:
        pool_length = int(raw_unit.options["pl"])
    except KeyError, ValueError:
        pool_length = None
    try:
        temperature = float(raw_unit.options["tmp"])
    except KeyError, ValueError:
        temperature = None
    return SwimmingUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=data.start_t,
        seconds=data.seconds,
        gym=data.gym,
        distance=distance,
        pool_length=pool_length,
        temperature=temperature,
        avg_hr=data.avg_hr,
        max_hr=data.max_hr,
        calories=data.calories,
    )


def build_skipping_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> RopeSkipUnit:
    data = parse_cardio_data(raw_unit.tokens, raw_unit.options)
    return RopeSkipUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        start_t=data.start_t,
        seconds=data.seconds,
        gym=data.gym,
        avg_hr=data.avg_hr,
        max_hr=data.max_hr,
        calories=data.calories,
    )
