from sqlalchemy.orm import Session

from bushido.modules.domain import Err, Result
from bushido.modules.gym.domain import GymUnitName
from bushido.modules.lifting.domain import LiftingUnitName
from bushido.modules.mapper import UnitMapper
from bushido.modules.parser import UnitParser
from bushido.modules.repo import UnitRepo
from bushido.modules.wimhof.domain import WimhofUnitName


def get_parser(unit_name: str) -> Result[UnitParser]:
    if unit_name in [un.name for un in GymUnitName]:
        pass
    elif unit_name in [un.name for un in LiftingUnitName]:
        pass
    elif unit_name in [un.name for un in WimhofUnitName]:
        pass
    else:
        return Err(message="No such unit name")


def get_mapper(unit_name: str) -> Result[UnitMapper]:
    if unit_name in [un.name for un in GymUnitName]:
        pass
    elif unit_name in [un.name for un in LiftingUnitName]:
        pass
    elif unit_name in [un.name for un in WimhofUnitName]:
        pass
    else:
        return Err(message="No such unit name")


def get_repo(unit_name: str, session: Session) -> Result[UnitRepo]:
    if unit_name in [un.name for un in GymUnitName]:
        pass
    elif unit_name in [un.name for un in LiftingUnitName]:
        pass
    elif unit_name in [un.name for un in WimhofUnitName]:
        pass
    else:
        return Err(message="No such unit name")
