from typing import override

from bushidolib.unit.cardio import RunningUnit, SwimmingUnit, RopeSkipUnit

from ..models import RunningUnitTable, SwimmingUnitTable, RopeSkipUnitTable
from ._base import BaseUnitRepo


class RunningUnitRepo(BaseUnitRepo[RunningUnit, RunningUnitTable]):
    orm_cls = RunningUnitTable

    @override
    def _to_orm(self, unit: RunningUnit) -> RunningUnitTable:
        return RunningUnitTable(
            log_time=unit.log_time,
            start_t=unit.start_t,
            seconds=unit.seconds,
            gym=unit.gym,
            distance=unit.distance,
            avg_hr=unit.avg_hr,
            max_hr=unit.max_hr,
            calories=unit.calories,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: RunningUnitTable) -> RunningUnit:
        return RunningUnit(
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

    @override
    def _to_orm(self, unit: SwimmingUnit) -> SwimmingUnitTable:
        return SwimmingUnitTable(
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
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: SwimmingUnitTable) -> SwimmingUnit:
        return SwimmingUnit(
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


class RopeSkipUnitRepo(BaseUnitRepo[RopeSkipUnit, RopeSkipUnitTable]):
    orm_cls = RopeSkipUnitTable

    @override
    def _to_orm(self, unit: RopeSkipUnit) -> RopeSkipUnitTable:
        return RopeSkipUnitTable(
            log_time=unit.log_time,
            start_t=unit.start_t,
            seconds=unit.seconds,
            gym=unit.gym,
            avg_hr=unit.avg_hr,
            max_hr=unit.max_hr,
            calories=unit.calories,
            comment=unit.comment,
        )

    @override
    def _from_orm(self, orm_unit: RopeSkipUnitTable) -> RopeSkipUnit:
        return RopeSkipUnit(
            start_t=orm_unit.start_t,
            seconds=orm_unit.seconds,
            gym=orm_unit.gym,
            avg_hr=orm_unit.avg_hr,
            max_hr=orm_unit.max_hr,
            calories=orm_unit.calories,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
