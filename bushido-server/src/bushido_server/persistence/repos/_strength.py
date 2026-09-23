from typing import override

from sqlalchemy.orm import selectinload

from bushidolib.unit.strength import LiftingSetData, LiftingUnit, StrengthUnit

from ..models import LiftingSet, LiftingUnitTable, StrengthUnitTable
from ._base import BaseUnitRepo


class StrengthUnitRepo(BaseUnitRepo[StrengthUnit, StrengthUnitTable]):
    orm_cls = StrengthUnitTable

    @override
    def _to_orm(self, unit: StrengthUnit) -> StrengthUnitTable:
        return StrengthUnitTable(
            log_time=unit.log_time,
            start_t=unit.start_t,
            end_t=unit.end_t,
            gym=unit.gym,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: StrengthUnitTable) -> StrengthUnit:
        return StrengthUnit(
            start_t=orm_unit.start_t,
            end_t=orm_unit.end_t,
            gym=orm_unit.gym,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )


class LiftingUnitRepo(BaseUnitRepo[LiftingUnit, LiftingUnitTable]):
    orm_cls = LiftingUnitTable
    load_options = (selectinload(LiftingUnitTable.subunits),)

    @override
    def _to_orm(self, unit: LiftingUnit) -> LiftingUnitTable:
        orm_unit = LiftingUnitTable(
            exercise=unit.exercise,
            variant=unit.variant,
            comment=unit.comment,
            log_time=unit.log_time,
        )
        orm_unit.subunits = [
            LiftingSet(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            for s in unit.sets
        ]
        return orm_unit

    @override
    def _from_orm(self, orm_unit: LiftingUnitTable) -> LiftingUnit:
        lst = []
        for s in orm_unit.subunits:
            sp = LiftingSetData(
                set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest
            )
            lst.append(sp)
        return LiftingUnit(
            exercise=orm_unit.exercise,
            variant=orm_unit.variant,
            sets=lst,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
