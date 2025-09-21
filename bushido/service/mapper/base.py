from typing import Protocol, TypeVar

from bushido.domain.base import ParsedUnit


T = TypeVar('T')


class UnitMapper(Protocol[T]):
    def to_orm(self, parsed_unit: ParsedUnit) -> list[T]:
        ...

    def from_orm(self, orm_lst: list[T]) -> ParsedUnit:
        ...

