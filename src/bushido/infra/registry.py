from sqlalchemy.orm import Session

from bushido.modules.domain import Err, Ok, Result, UnitData
from bushido.modules.gym.domain import GymUnitName
from bushido.modules.gym.mapper import GymMapper
from bushido.modules.gym.orm import GymUnit
from bushido.modules.gym.parser import GymParser
from bushido.modules.lifting.domain import LiftingUnitName
from bushido.modules.lifting.mapper import LiftingMapper
from bushido.modules.lifting.orm import LiftingUnit
from bushido.modules.lifting.parser import LiftingParser
from bushido.modules.mapper import UnitMapper
from bushido.modules.parser import UnitParser
from bushido.modules.repo import UnitRepo
from bushido.modules.wimhof.domain import WimhofUnitName
from bushido.modules.wimhof.mapper import WimhofMapper
from bushido.modules.wimhof.orm import WimhofUnit
from bushido.modules.wimhof.parser import WimhofParser


def get_parser(unit_name: str) -> Result[UnitParser[UnitData]]:
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


def get_repo(unit_name: str, session: Session) -> Result[UnitRepo]:
    if unit_name in [un.name for un in GymUnitName]:
        return Ok(UnitRepo(session=session, unit_cls=GymUnit))
    elif unit_name in [un.name for un in LiftingUnitName]:
        return Ok(
            UnitRepo(
                session=session, unit_cls=LiftingUnit, subrels=LiftingUnit.subunits
            )
        )
    elif unit_name in [un.name for un in WimhofUnitName]:
        return Ok(
            UnitRepo(session=session, unit_cls=WimhofUnit, subrels=WimhofUnit.subunits)
        )
    else:
        return Err(message="No such unit name")
