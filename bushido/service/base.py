from typing import Generic

from sqlalchemy.orm import Session

from bushido.core.result import Err, Ok, Result
from bushido.domain.unit import UNIT_T
from bushido.iface.mapper.unit import CompoundUnitMapper, UnitMapper
from bushido.iface.parser.unit import UnitParser
from bushido.iface.parser.utils import preprocess_input
from bushido.infra.repo.unit import (
    CUT_ORM,
    SUT_ORM,
    UT_ORM,
    CompoundUnitRepo,
    UnitRepo,
)


# TODO duplicated code
class LogUnitService(Generic[UNIT_T, UT_ORM]):
    def __init__(
        self,
        parser: UnitParser[UNIT_T],
        mapper: UnitMapper[UNIT_T, UT_ORM],
        unit_repo: UnitRepo[UT_ORM].__class__,
    ):
        self._parser = parser
        self._mapper = mapper
        self._repo = unit_repo

    def log_unit(self, line: str, session: Session) -> Result[str]:
        pre_result = preprocess_input(line)
        if isinstance(pre_result, Err):
            return Err('preprocess error')

        unit_spec = pre_result.value
        parse_result = self._parser.parse(unit_spec)
        if isinstance(parse_result, Err):
            return Err('parse error')

        parsed_unit = parse_result.value
        unit = self._mapper.to_orm(parsed_unit)
        unit_repo = self._repo(session)
        if unit_repo.add_unit(unit):
            return Ok('success')
        else:
            return Err('error')


class LogCompoundUnitService(Generic[UNIT_T, CUT_ORM, SUT_ORM]):
    def __init__(
        self,
        parser: UnitParser[UNIT_T],
        mapper: CompoundUnitMapper[UNIT_T, CUT_ORM, SUT_ORM],
        repo: CompoundUnitRepo[CUT_ORM, SUT_ORM].__class__,
    ):
        self._parser = parser
        self._mapper = mapper
        self._repo = repo

    def log_unit(self, line: str, session: Session) -> Result[str]:
        pre_result = preprocess_input(line)
        if isinstance(pre_result, Err):
            return Err('preprocess error')

        unit_spec = pre_result.value
        parse_result = self._parser.parse(unit_spec)
        if isinstance(parse_result, Err):
            return Err('parse error')

        parsed_unit = parse_result.value
        unit, subunits = self._mapper.to_orm(parsed_unit)
        unit_repo = self._repo(session)
        if unit_repo.add_compound_unit(unit, subunits):
            return Ok('success')
        else:
            return Err('error')
