from sqlalchemy.orm import Session

from bushido.core.conf import UnitCategory
from bushido.core.result import Err, Ok, Result
from bushido.iface.mapper.lifting import LiftingMapper
from bushido.iface.parser.lifting import LiftingParser
from bushido.infra.db import LiftingSet, LiftingUnit
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
                repo = UnitRepo[LiftingUnit, LiftingSet](session)
                # TODO mypy is fine, pycharm not
                return Ok(LogUnitService(parser, mapper, repo))
            case _:
                return Err('no such unit category')
