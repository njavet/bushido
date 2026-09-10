from dataclasses import dataclass

from bushidolib.category.cardio import CardioData
from bushidolib.category.gym import GymData
from bushidolib.category.lifting import LiftingData
from bushidolib.category.wimhof import WimhofData
from bushidolib.exceptions import UnitParsingError


@dataclass(frozen=True, slots=True)
class RawUnit:
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None


UnitData = CardioData | GymData | LiftingData | WimhofData


@dataclass(frozen=True, slots=True)
class Unit:
    data: UnitData
    comment: str | None


def parse_raw_unit(line: str) -> RawUnit:
    body, sep, comment = line.partition("#")
    raw_tokens = tuple(body.split())

    if not raw_tokens:
        raise UnitParsingError(f"Empty unit line: {line}")

    return RawUnit(
        name=raw_tokens[0],
        tokens=tuple(raw_tokens[1:]),
        comment=comment.strip() if sep and comment.strip() else None,
    )
