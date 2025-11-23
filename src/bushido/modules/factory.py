from typing import Any

from sqlalchemy.orm import Session

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
        self.parser = self.get_parsers()
        self.mappers = self.get_mappers()

    @staticmethod
    def get_parsers() -> dict[str, Any]:
        result: dict[str, Any] = {}
        for unit_name in GymUnitName.__members__:
            result[unit_name] = GymParser(unit_name=unit_name)
        for unit_name in LiftingUnitName.__members__:
            result[unit_name] = LiftingParser(unit_name=unit_name)
        for unit_name in WimhofUnitName.__members__:
            result[unit_name] = WimhofParser(unit_name=unit_name)
        return result

    @staticmethod
    def get_mappers() -> dict[str, Any]:
        result: dict[str, Any] = {}
        for unit_name in GymUnitName.__members__:
            result[unit_name] = GymMapper()
        for unit_name in LiftingUnitName.__members__:
            result[unit_name] = LiftingMapper()
        for unit_name in WimhofUnitName.__members__:
            result[unit_name] = WimhofMapper()
        return result

    @staticmethod
    def get_repo(unit_name: str, session: Session) -> Any:
        if unit_name in [un.name for un in GymUnitName]:
            return UnitRepo[GymUnit, Any](session=session, unit_cls=GymUnit)
        elif unit_name in [un.name for un in LiftingUnitName]:
            return UnitRepo[LiftingUnit, LiftingSet](
                session=session, unit_cls=LiftingUnit, subrels=LiftingUnit.subunits
            )
        elif unit_name in [un.name for un in WimhofUnitName]:
            return UnitRepo[WimhofUnit, WimhofRound](
                session=session, unit_cls=WimhofUnit, subrels=WimhofUnit.subunits
            )
