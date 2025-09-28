from types import MappingProxyType
from typing import Any, Mapping

from bushido.core.unit import LiftingUnitName
from bushido.core.types import ORM_T
from bushido.infra.db import LiftingSet
from bushido.iface.mapper import LiftingMapper
from bushido.iface.mapper.unit import UnitMapper
from bushido.iface.parser.lifting import LiftingParser
from bushido.iface.parser.unit import UnitParser


# TODO check return type (any vs UNIT_T)
def load_parsers() -> Mapping[str, UnitParser[Any]]:
    lifting_parsers = {u.name: LiftingParser() for u in LiftingUnitName}
    return MappingProxyType(lifting_parsers)


def load_mappers() -> Mapping[str, UnitMapper[Any, Any]]:
    lifting_mappers = {u.name: LiftingMapper() for u in LiftingUnitName}
    return MappingProxyType(lifting_mappers)


def load_subunit_cls() -> Mapping[str, Any]:
    lifting_subunit_cls = {u.name: LiftingSet for u in LiftingUnitName}
    return MappingProxyType(lifting_subunit_cls)
