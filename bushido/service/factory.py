from sqlalchemy.orm import Session

from bushido.core.unit import LiftingUnitName
from bushido.infra.repo.unit import UnitRepo
from bushido.infra.db import LiftingUnit, LiftingSet
from bushido.iface.parser.lifting import LiftingParser
from bushido.iface.mapper.lifting import LiftingMapper
from bushido.service.base import LogUnitService


class ServiceFactory:
    def get_service(self, unit_name: str, session: Session) -> LogUnitService:
        if unit_name in [u.name for u in LiftingUnitName]:
            parser = LiftingParser()
            mapper = LiftingMapper()
            repo = UnitRepo[LiftingUnit, LiftingSet](session)
            return LogUnitService(parser, mapper, repo)



