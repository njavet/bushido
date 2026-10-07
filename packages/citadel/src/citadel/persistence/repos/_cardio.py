from typing import override

from citadel.domain.unit import RopeSkipUnit, RunningUnit, SwimmingUnit, UnitType

from ..models import RopeSkipUnitTable, RunningUnitTable, SwimmingUnitTable, UnitTable
from ._base import BaseUnitRepo


class RunningUnitRepo(BaseUnitRepo[RunningUnit]):
    unit_type = UnitType.running

    @override
    def add_unit(self, unit: RunningUnit, spartan_id: int) -> None:
        orm_unit = UnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            running=RunningUnitTable(
                start_t=unit.start_t,
                seconds=unit.seconds,
                gym=unit.gym,
                distance=unit.distance,
                avg_hr=unit.avg_hr,
                max_hr=unit.max_hr,
                calories=unit.calories,
            ),
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: UnitTable) -> RunningUnit:
        assert orm_unit.running is not None
        return RunningUnit(
            name=orm_unit.name,
            start_t=orm_unit.running.start_t,
            seconds=orm_unit.running.seconds,
            gym=orm_unit.running.gym,
            distance=orm_unit.running.distance,
            avg_hr=orm_unit.running.avg_hr,
            max_hr=orm_unit.running.max_hr,
            calories=orm_unit.running.calories,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )


class SwimmingUnitRepo(BaseUnitRepo[SwimmingUnit]):
    unit_type = UnitType.swimming

    @override
    def add_unit(self, unit: SwimmingUnit, spartan_id: int) -> None:
        orm_unit = UnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            swimming=SwimmingUnitTable(
                start_t=unit.start_t,
                seconds=unit.seconds,
                gym=unit.gym,
                distance=unit.distance,
                pool_length=unit.pool_length,
                temperature=unit.temperature,
                avg_hr=unit.avg_hr,
                max_hr=unit.max_hr,
                calories=unit.calories,
            ),
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: UnitTable) -> SwimmingUnit:
        assert orm_unit.swimming is not None
        return SwimmingUnit(
            name=orm_unit.name,
            start_t=orm_unit.swimming.start_t,
            seconds=orm_unit.swimming.seconds,
            gym=orm_unit.swimming.gym,
            distance=orm_unit.swimming.distance,
            pool_length=orm_unit.swimming.pool_length,
            temperature=orm_unit.swimming.temperature,
            avg_hr=orm_unit.swimming.avg_hr,
            max_hr=orm_unit.swimming.max_hr,
            calories=orm_unit.swimming.calories,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )


class RopeSkipUnitRepo(BaseUnitRepo[RopeSkipUnit]):
    unit_type = UnitType.skipping

    @override
    def add_unit(self, unit: RopeSkipUnit, spartan_id: int) -> None:
        orm_unit = UnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            comment=unit.comment,
            log_time=unit.log_time,
            skipping=RopeSkipUnitTable(
                start_t=unit.start_t,
                seconds=unit.seconds,
                gym=unit.gym,
                avg_hr=unit.avg_hr,
                max_hr=unit.max_hr,
                calories=unit.calories,
            ),
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: UnitTable) -> RopeSkipUnit:
        assert orm_unit.skipping is not None
        return RopeSkipUnit(
            name=orm_unit.name,
            start_t=orm_unit.skipping.start_t,
            seconds=orm_unit.skipping.seconds,
            gym=orm_unit.skipping.gym,
            avg_hr=orm_unit.skipping.avg_hr,
            max_hr=orm_unit.skipping.max_hr,
            calories=orm_unit.skipping.calories,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
