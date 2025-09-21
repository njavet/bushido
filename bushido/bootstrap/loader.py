from types import MappingProxyType
from typing import Any, Mapping

# project imports
from bushido.core.unit import LiftingUnitName
from bushido.service.mapper.base import UnitMapper
from bushido.service.mapper.lifting import LiftingMapper
from bushido.service.parser.base import UnitParser
from bushido.service.parser.lifting import LiftingParser


# TODO check return type (any vs UNIT_T)
def load_parsers() -> Mapping[str, UnitParser[Any]]:
    lifting_parsers = {u.name: LiftingParser() for u in LiftingUnitName}
    return MappingProxyType(lifting_parsers)


def load_mappers() -> Mapping[str, UnitMapper[Any, Any, Any]]:
    lifting_mappers = {u.name: LiftingMapper() for u in LiftingUnitName}
    return MappingProxyType(lifting_mappers)
