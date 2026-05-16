from typing import Protocol

from bushido.units.base import TU, P, T, Unit


class UnitMapper(Protocol[T, TU]):
    @staticmethod
    def to_orm(unit: Unit[T]) -> TU: ...

    @staticmethod
    def from_orm(orm_unit: TU) -> Unit[T]: ...


class UnitParser(Protocol[P]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> P: ...
