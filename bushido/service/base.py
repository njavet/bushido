from typing import Generic

from sqlalchemy.orm import Session

from bushido.core.result import Result, Err, Ok
from bushido.domain.unit import UNIT_T
from bushido.iface.parser.unit import UnitParser
from bushido.iface.parser.utils import preprocess_input
from bushido.iface.mapper.unit import UnitMapper, CompoundUnitMapper
from bushido.infra.repo.unit import UT_ORM, CUT_ORM, SUT_ORM, UnitRepo, CompoundUnitRepo


class LogUnitService(Generic[UNIT_T, UT_ORM]):
    def __init__(self, parser: UnitParser[UNIT_T], mapper: UnitMapper[UNIT_T, UT_ORM]):
        self._parser = parser
        self._mapper = mapper

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
        unit_repo = UnitRepo(session)
        if unit_repo.add_unit(unit):
            return Ok('success')
        else:
            return Err('error')


class LogCompoundUnitService(Generic[UNIT_T, CUT_ORM, SUT_ORM]):
    def __init__(self, parser: UnitParser[UNIT_T], mapper: CompoundUnitMapper[UNIT_T, CUT_ORM, SUT_ORM]):
        self._parser = parser
        self._mapper = mapper

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
        unit_repo = CompoundUnitRepo(session)
        if unit_repo.add_compound_unit(unit, subunits):
            return Ok('success')
        else:
            return Err('error')
