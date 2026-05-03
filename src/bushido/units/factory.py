from typing import Any

from sqlalchemy.orm import Session

from bushido.units.cardio import CardioMapper, CardioParser, CardioUnitName
from bushido.units.gym import GymMapper, GymParser, GymUnit, GymUnitName
from bushido.units.lifting import (
    LiftingMapper,
    LiftingParser,
    LiftingSet,
    LiftingUnit,
    LiftingUnitName,
)
from bushido.units.mapper import UnitMapper
from bushido.units.parsing.base import UnitParser
from bushido.units.repo import UnitRepo
from bushido.units.wimhof import (
    WimhofMapper,
    WimhofParser,
    WimhofRound,
    WimhofUnit,
    WimhofUnitName,
)

PARSERS: dict[str, UnitParser[Any]] = {
    **{u.name: GymParser() for u in GymUnitName},
    **{u.name: CardioParser() for u in CardioUnitName},
    **{u.name: LiftingParser() for u in LiftingUnitName},
    **{u.name: WimhofParser() for u in WimhofUnitName},
}


MAPPERS: dict[str, UnitMapper[Any, Any, Any]] = {
    **{u.name: GymMapper() for u in GymUnitName},
    **{u.name: CardioMapper() for u in CardioUnitName},
    **{u.name: LiftingMapper() for u in LiftingUnitName},
    **{u.name: WimhofMapper() for u in WimhofUnitName},
}


def get_unit_names() -> list[str]:
    return list(PARSERS.keys())


def get_parser(unit_name: str) -> UnitParser[Any]:
    # unit_name must be validated, therefore, raise if not known
    try:
        parser = PARSERS[unit_name]
    except KeyError:
        raise ValueError(f"Unknown unit: {unit_name}")
    return parser


def get_mapper(unit_name: str) -> UnitMapper[Any, Any, Any]:
    # unit_name must be validated, therefore, raise if not known
    try:
        mapper = MAPPERS[unit_name]
    except KeyError:
        raise ValueError(f"Unknown unit: {unit_name}")
    return mapper


def get_repo(unit_name: str, session: Session) -> UnitRepo[Any, Any]:
    # unit_name must be validated, therefore, raise if not known
    if unit_name in GymUnitName.__members__:
        return UnitRepo[GymUnit, Any](session=session, unit_cls=GymUnit)
    elif unit_name in LiftingUnitName.__members__:
        return UnitRepo[LiftingUnit, LiftingSet](
            session=session, unit_cls=LiftingUnit, subrels=LiftingUnit.subunits
        )
    elif unit_name in WimhofUnitName.__members__:
        return UnitRepo[WimhofUnit, WimhofRound](
            session=session, unit_cls=WimhofUnit, subrels=WimhofUnit.subunits
        )
    else:
        raise ValueError(f"Unknown unit: {unit_name}")
