from types import MappingProxyType
from typing import Any, Mapping

from bushido.core.unit import LiftingUnitName
from bushido.iface.mapper import LiftingMapper
from bushido.iface.mapper.base import UnitMapper
from bushido.iface.parser.base import UnitParser
from bushido.iface.parser.lifting import LiftingParser


# TODO check return type (any vs UNIT_T)
def load_parsers() -> Mapping[str, UnitParser[Any]]:
    lifting_parsers = {u.name: LiftingParser() for u in LiftingUnitName}
    return MappingProxyType(lifting_parsers)


def load_mappers() -> Mapping[str, UnitMapper[Any, Any, Any]]:
    lifting_mappers = {u.name: LiftingMapper() for u in LiftingUnitName}
    return MappingProxyType(lifting_mappers)
