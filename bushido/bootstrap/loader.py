# project imports
from bushido.core.unit import LiftingUnitName
from bushido.service.parser.lifting import LiftingParser
from bushido.service.mapper.lifting import LiftingMapper


def load_parsers() -> dict:
    lifting_parsers = {u.name: LiftingParser for u in LiftingUnitName}
    return lifting_parsers


def load_mappers() -> dict:
    lifting_mappers = {u.name: LiftingMapper for u in LiftingUnitName}
    return lifting_mappers
