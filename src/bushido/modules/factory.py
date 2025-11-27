from typing import Any

from sqlalchemy.orm import Session

from bushido.core.dtypes import UnitMapper
from bushido.modules.gym import GymMapper, GymParser, GymUnit, GymUnitName
from bushido.modules.lifting import (
    LiftingMapper,
    LiftingParser,
    LiftingSet,
    LiftingUnit,
    LiftingUnitName,
)
from bushido.modules.parser import UnitParser
from bushido.modules.repo import UnitRepo
from bushido.modules.wimhof import (
    WimhofMapper,
    WimhofParser,
    WimhofRound,
    WimhofUnit,
    WimhofUnitName,
)

PARSERS: dict[str, UnitParser[Any]] = {
    **{u.name: GymParser(u.name) for u in GymUnitName},
    **{u.name: LiftingParser(u.name) for u in LiftingUnitName},
    **{u.name: WimhofParser(u.name) for u in WimhofUnitName},
}


MAPPERS: dict[str, UnitMapper[Any, Any, Any]] = {
    **{u.name: GymMapper() for u in GymUnitName},
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
