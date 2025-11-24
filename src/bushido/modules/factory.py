from typing import Any

from sqlalchemy.orm import Session

from bushido.modules.dtypes import Err, Ok, Result
from bushido.modules.gym import GymMapper, GymParser, GymUnit, GymUnitName
from bushido.modules.lifting import (
    LiftingMapper,
    LiftingParser,
    LiftingSet,
    LiftingUnit,
    LiftingUnitName,
)
from bushido.modules.repo import UnitRepo
from bushido.modules.wimhof import (
    WimhofMapper,
    WimhofParser,
    WimhofRound,
    WimhofUnit,
    WimhofUnitName,
)


class Factory:
    def __init__(self) -> None:
        self.parsers = {
            **{u.name: GymParser(u.name) for u in GymUnitName},
            **{u.name: LiftingParser(u.name) for u in LiftingUnitName},
            **{u.name: WimhofParser(u.name) for u in WimhofUnitName},
        }
        self.mappers = {
            **{u.name: GymMapper() for u in GymUnitName},
            **{u.name: LiftingMapper() for u in LiftingUnitName},
            **{u.name: WimhofMapper() for u in WimhofUnitName},
        }

    def get_parser(self, unit_name: str) -> Result[object]:
        parser = self.parsers.get(unit_name)
        if parser is None:
            return Err(message=f"Unknown unit: {unit_name}")
        return Ok(parser)

    def get_mapper(self, unit_name: str) -> Result[object]:
        mapper = self.mappers.get(unit_name)
        if mapper is None:
            return Err(message=f"Unknown unit: {unit_name}")
        return Ok(mapper)

    def get_repo(self, unit_name: str, session: Session) -> Result[UnitRepo[Any, Any]]:
        if unit_name in GymUnitName.__members__:
            return Ok(UnitRepo[GymUnit, Any](session=session, unit_cls=GymUnit))
        elif unit_name in LiftingUnitName.__members__:
            return Ok(
                UnitRepo[LiftingUnit, LiftingSet](
                    session=session, unit_cls=LiftingUnit, subrels=LiftingUnit.subunits
                )
            )
        elif unit_name in WimhofUnitName.__members__:
            return Ok(
                UnitRepo[WimhofUnit, WimhofRound](
                    session=session, unit_cls=WimhofUnit, subrels=WimhofUnit.subunits
                )
            )
        else:
            return Err(message=f"Unknown unit: {unit_name}")
