from typing import override

from bushidolib.unit.chrono import ChronoUnit

from ..models import ChronoUnitTable
from ._base import BaseUnitRepo


class ChronoUnitRepo(BaseUnitRepo[ChronoUnit, ChronoUnitTable]):
    orm_cls = ChronoUnitTable

    @override
    def _to_orm(self, unit: ChronoUnit) -> ChronoUnitTable:
        return ChronoUnitTable(
            name=unit.name,
            seconds=unit.seconds,
            log_time=unit.log_time,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: ChronoUnitTable) -> ChronoUnit:
        return ChronoUnit(
            name=orm_unit.name,
            seconds=orm_unit.seconds,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
