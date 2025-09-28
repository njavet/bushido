from typing import Any

from sqlalchemy.orm import Session

from bushido.core.conf import UnitCategory
from bushido.core.result import Err, Ok, Result
from bushido.iface.mapper import GymMapper, LiftingMapper
from bushido.iface.parser import GymParser, LiftingParser
from bushido.infra.db import GymUnit, LiftingSet, LiftingUnit
from bushido.infra.repo.unit import UnitRepo
from bushido.service.base import LogUnitService


class ServiceFactory:
    def get_service(
        self, unit_category: UnitCategory, session: Session
    ) -> Result[LogUnitService]:
        match unit_category:
            case UnitCategory.lifting:
                parser = LiftingParser()
                mapper = LiftingMapper()
                repo = UnitRepo[LiftingUnit, LiftingSet](
                    session, LiftingUnit, LiftingUnit.subunits
                )
                # TODO mypy is fine, pycharm not
                return Ok(LogUnitService(parser, mapper, repo))
            case UnitCategory.gym:
                parser = GymParser()
                mapper = GymMapper()
                repo = UnitRepo[GymUnit, Any](session, GymUnit, list[Any])
                return Ok(LogUnitService(parser, mapper, repo))
            case _:
                return Err('no such unit category')
