from typing import Protocol

from bushido.domain.base import UNIT_T, ParsedUnit
from bushido.infra.repo.unit import S, U


class UnitMapper(Protocol[UNIT_T, U, S]):
    def to_orm(self, parsed_unit: ParsedUnit[UNIT_T]) -> tuple[U, list[S]]: ...

    def from_orm(self, orms: tuple[U, list[S]]) -> ParsedUnit[UNIT_T]: ...
