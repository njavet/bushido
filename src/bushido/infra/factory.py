from typing import Any

from sqlalchemy.orm import Session

from bushido.infra.db import GymUnit, LiftingSet, LiftingUnit, WimhofUnit
from bushido.modules.domain import Err, Ok, Result, UnitCategory
from bushido.modules.repo import UnitRepo
from bushido.service.log_unit import LogUnitService


class ServiceFactory:
    def get_service(
        self, unit_category: UnitCategory, session: Session
    ) -> Result[LogUnitService]:
        match unit_category:
            case UnitCategory.lifting:
                lifting_parser = LiftingParser()
                lifting_mapper = LiftingMapper()
                lifting_repo = UnitRepo[LiftingUnit, LiftingSet](
                    session, LiftingUnit, LiftingUnit.subunits
                )
                # TODO mypy is fine, pycharm not
                return Ok(LogUnitService(lifting_parser, lifting_mapper, lifting_repo))
            case UnitCategory.gym:
                gym_parser = GymParser()
                gym_mapper = GymMapper()
                gym_repo = UnitRepo[GymUnit, Any](session, GymUnit, None)
                return Ok(LogUnitService(gym_parser, gym_mapper, gym_repo))
            case UnitCategory.wimhof:
                wimhof_parser = WimhofParser()
                wimhof_mapper = WimhofMapper()
                wimhof_repo = UnitRepo[WimhofUnit, Any](session, WimhofUnit, None)
                return Ok(LogUnitService(wimhof_parser, wimhof_mapper, wimhof_repo))
            case _:
                return Err("no such unit category")
