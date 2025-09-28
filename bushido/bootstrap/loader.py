from types import MappingProxyType
from typing import Mapping

from bushido.core.types import ORM_T, UNIT_T
from bushido.core.unit import LiftingUnitName
from bushido.iface.mapper import LiftingMapper
from bushido.iface.mapper.unit import UnitMapper
from bushido.iface.parser.lifting import LiftingParser
from bushido.iface.parser.unit import UnitParser


# TODO check return type (any vs UNIT_T)
def load_parsers() -> Mapping[str, UnitParser[UNIT_T]]:
    lifting_parsers = {u.name: LiftingParser() for u in LiftingUnitName}
    return MappingProxyType(lifting_parsers)


def load_mappers() -> Mapping[str, UnitMapper[UNIT_T, ORM_T]]:
    lifting_mappers = {u.name: LiftingMapper() for u in LiftingUnitName}
    return MappingProxyType(lifting_mappers)
