from types import MappingProxyType

from bushido.core.unit import LiftingUnitName
from bushido.iface.mapper import LiftingMapper
from bushido.iface.parser.lifting import LiftingParser
from bushido.infra.repo.unit import UnitRepo, CompoundUnitRepo
from bushido.service.base import LogCompoundUnitService


def load_log_services():
    parser = LiftingParser()
    mapper = LiftingMapper()
    lifting_services = {u.name: LogCompoundUnitService(parser, mapper, CompoundUnitRepo) for u in LiftingUnitName}
    return MappingProxyType(lifting_services)
