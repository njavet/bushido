from typing import override

from bushidolib.unit.martial_arts import MartialArtsUnit

from ..models import MartialArtsUnitTable
from ._base import BaseUnitRepo


class MartialArtsUnitRepo(BaseUnitRepo[MartialArtsUnit, MartialArtsUnitTable]):
    orm_cls = MartialArtsUnitTable

    @override
    def _to_orm(self, unit: MartialArtsUnit) -> MartialArtsUnitTable:
        return MartialArtsUnitTable(
            kind=unit.kind,
            log_time=unit.log_time,
            start_t=unit.start_t,
            end_t=unit.end_t,
            gym=unit.gym,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: MartialArtsUnitTable) -> MartialArtsUnit:
        return MartialArtsUnit(
            kind=orm_unit.kind,
            start_t=orm_unit.start_t,
            end_t=orm_unit.end_t,
            gym=orm_unit.gym,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
