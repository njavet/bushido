from typing import override

from citadel.unit import UnitType
from citadel.unit.cardio import RunningUnit, SkippingUnit, SwimmingUnit

from ..models import RunningUnitTable, SkippingUnitTable, SwimmingUnitTable
from ._base import BaseUnitRepo


class RunningUnitRepo(BaseUnitRepo[RunningUnit, RunningUnitTable]):
    orm_cls = RunningUnitTable
    unit_type = UnitType.running

    @override
    def add_unit(self, unit: RunningUnit, spartan_id: int) -> None:
        orm_unit = RunningUnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            start_t=unit.start_t,
            seconds=unit.seconds,
            gym=unit.gym,
            distance=unit.distance,
            avg_hr=unit.avg_hr,
            max_hr=unit.max_hr,
            calories=unit.calories,
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: RunningUnitTable) -> RunningUnit:
        return RunningUnit(
            name=orm_unit.name,
            start_t=orm_unit.start_t,
            seconds=orm_unit.seconds,
            gym=orm_unit.gym,
            distance=orm_unit.distance,
            avg_hr=orm_unit.avg_hr,
            max_hr=orm_unit.max_hr,
            calories=orm_unit.calories,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )


class SwimmingUnitRepo(BaseUnitRepo[SwimmingUnit, SwimmingUnitTable]):
    orm_cls = SwimmingUnitTable
    unit_type = UnitType.swimming

    @override
    def add_unit(self, unit: SwimmingUnit, spartan_id: int) -> None:
        orm_unit = SwimmingUnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            start_t=unit.start_t,
            seconds=unit.seconds,
            gym=unit.gym,
            distance=unit.distance,
            pool_length=unit.pool_length,
            temperature=unit.temperature,
            avg_hr=unit.avg_hr,
            max_hr=unit.max_hr,
            calories=unit.calories,
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: SwimmingUnitTable) -> SwimmingUnit:
        return SwimmingUnit(
            name=orm_unit.name,
            start_t=orm_unit.start_t,
            seconds=orm_unit.seconds,
            gym=orm_unit.gym,
            distance=orm_unit.distance,
            pool_length=orm_unit.pool_length,
            temperature=orm_unit.temperature,
            avg_hr=orm_unit.avg_hr,
            max_hr=orm_unit.max_hr,
            calories=orm_unit.calories,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )


class SkippingUnitRepo(BaseUnitRepo[SkippingUnit, SkippingUnitTable]):
    orm_cls = SkippingUnitTable
    unit_type = UnitType.skipping

    @override
    def add_unit(self, unit: SkippingUnit, spartan_id: int) -> None:
        orm_unit = SkippingUnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            start_t=unit.start_t,
            seconds=unit.seconds,
            gym=unit.gym,
            avg_hr=unit.avg_hr,
            max_hr=unit.max_hr,
            calories=unit.calories,
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: SkippingUnitTable) -> SkippingUnit:
        return SkippingUnit(
            name=orm_unit.name,
            start_t=orm_unit.start_t,
            seconds=orm_unit.seconds,
            gym=orm_unit.gym,
            avg_hr=orm_unit.avg_hr,
            max_hr=orm_unit.max_hr,
            calories=orm_unit.calories,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
