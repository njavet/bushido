from typing import Any

from sqlalchemy.orm import Session

from bushido.modules.dtypes import Err, Result
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
    # TODO redesign
    def __init__(self):
        self.gym_parsers = {
            unit_name: GymParser(unit_name=unit_name)
            for unit_name in GymUnitName.__members__
        }
        self.lifting_parsers = {
            unit_name: LiftingParser(unit_name=unit_name)
            for unit_name in LiftingUnitName.__members__
        }
        self.wimhof_parsers = {
            unit_name: WimhofParser(unit_name=unit_name)
            for unit_name in WimhofUnitName.__members__
        }
        self.gym_mappers = {
            unit_name: GymMapper() for unit_name in GymUnitName.__members__
        }
        self.lifting_mappers = {
            unit_name: LiftingMapper() for unit_name in LiftingUnitName.__members__
        }
        self.wimhof_mappers = {
            unit_name: WimhofMapper() for unit_name in WimhofUnitName.__members__
        }

    def get_parser(self, unit_name: str) -> Result[Any]:
        if unit_name in self.gym_parsers:
            return Result(self.gym_parsers[unit_name])
        elif unit_name in self.lifting_parsers:
            return Result(self.lifting_parsers[unit_name])
        elif unit_name in self.wimhof_parsers:
            return Result(self.wimhof_parsers[unit_name])
        else:
            return Err(message=f"Unknown unit: {unit_name}")

    def get_mapper(self, unit_name: str) -> Result[Any]:
        if unit_name in self.gym_mappers:
            return Result(self.gym_mappers[unit_name])
        elif unit_name in self.lifting_mappers:
            return Result(self.lifting_parsers[unit_name])
        elif unit_name in self.wimhof_mappers:
            return Result(self.wimhof_mappers[unit_name])
        else:
            return Err(message=f"Unknown unit: {unit_name}")

    def get_repo(self, unit_name: str, session: Session) -> Result[Any]:
        if unit_name in self.gym_parsers:
            return Result(UnitRepo[GymUnit, Any](session=session, unit_cls=GymUnit))
        elif unit_name in self.lifting_parsers:
            return Result(
                UnitRepo[LiftingUnit, LiftingSet](
                    session=session, unit_cls=LiftingUnit, subrels=LiftingUnit.subunits
                )
            )
        elif unit_name in self.wimhof_parsers:
            return Result(
                UnitRepo[WimhofUnit, WimhofRound](
                    session=session, unit_cls=WimhofUnit, subrels=WimhofUnit.subunits
                )
            )
        else:
            return Err(message=f"Unknown unit: {unit_name}")
