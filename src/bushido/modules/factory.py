from typing import Any

from sqlalchemy.orm import Session

from bushido.modules.dtypes import UnitData, UnitMapper
from bushido.modules.parser import UnitParser


class Factory:
    def __init__(self) -> None:
        self.parser = self.get_parser()
        self.mappers = self.get_mappers()

    def get_parsers(self) -> dict[str, UnitParser[UnitData]]:
        if unit_name in [un.name for un in GymUnitName]:
            return Ok(GymParser(unit_name=unit_name))
        elif unit_name in [un.name for un in LiftingUnitName]:
            return Ok(LiftingParser(unit_name=unit_name))
        elif unit_name in [un.name for un in WimhofUnitName]:
            return Ok(WimhofParser(unit_name=unit_name))
        else:
            return Err(message="No such unit name")

    def get_mapper(unit_name: str) -> Result[UnitMapper]:
        if unit_name in [un.name for un in GymUnitName]:
            return Ok(GymMapper())
        elif unit_name in [un.name for un in LiftingUnitName]:
            return Ok(LiftingMapper())
        elif unit_name in [un.name for un in WimhofUnitName]:
            return Ok(WimhofMapper())
        else:
            return Err(message="No such unit name")

    def get_repo(unit_name: str, session: Session) -> Result[UnitRepo[UnitData]]:
        if unit_name in [un.name for un in GymUnitName]:
            return Ok(UnitRepo[GymUnit, Any](session=session, unit_cls=GymUnit))
        elif unit_name in [un.name for un in LiftingUnitName]:
            return Ok(
                UnitRepo[LiftingUnit, LiftingSet](
                    session=session, unit_cls=LiftingUnit, subrels=LiftingUnit.subunits
                )
            )
        elif unit_name in [un.name for un in WimhofUnitName]:
            return Ok(
                UnitRepo[WimhofUnit, WimhofRound](
                    session=session, unit_cls=WimhofUnit, subrels=WimhofUnit.subunits
                )
            )
        else:
            return Err(message="No such unit name")
