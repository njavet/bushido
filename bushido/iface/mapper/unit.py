from typing import Protocol

from bushido.domain.unit import UNIT_T, ParsedUnit
from bushido.infra.repo.unit import CUT_ORM, SUT_ORM, UT_ORM


class UnitMapper(Protocol[UNIT_T, UT_ORM]):
    def to_orm(self, parsed_unit: ParsedUnit[UNIT_T]) -> UT_ORM: ...

    def from_orm(self, orm: UT_ORM) -> ParsedUnit[UNIT_T]: ...


class CompoundUnitMapper(Protocol[UNIT_T, CUT_ORM, SUT_ORM]):
    def to_orm(
        self, parsed_unit: ParsedUnit[UNIT_T]
    ) -> tuple[CUT_ORM, list[SUT_ORM]]: ...

    def from_orm(self, orm: tuple[CUT_ORM, list[SUT_ORM]]) -> ParsedUnit[UNIT_T]: ...
