from typing import Any

from bushido.core.dtypes import ParsedUnit
from bushido.modules.mapper import UnitMapper

from .domain import WorkSpec
from .orm import WorkUnit


class WorkMapper(UnitMapper[WorkSpec, WorkUnit, Any]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[WorkSpec]) -> tuple[WorkUnit, list[Any]]:
        unit = WorkUnit(
            name=parsed_unit.name,
            log_time=parsed_unit.log_time,
            start_t=parsed_unit.data.start_t,
            end_t=parsed_unit.data.end_t,
            location=parsed_unit.data.location,
            employer=parsed_unit.data.employer,
            project=parsed_unit.data.project,
            comment=parsed_unit.comment,
        )
        return unit, []

    # TODO fix Any / None / []
    @staticmethod
    def from_orm(orms: tuple[WorkUnit, list[Any]]) -> ParsedUnit[WorkSpec]:
        unit, _ = orms
        pu = ParsedUnit(
            name=unit.name,
            data=WorkSpec(
                start_t=unit.start_t,
                end_t=unit.end_t,
                location=unit.location,
                employer=unit.employer,
                project=unit.project,
            ),
            log_time=unit.log_time,
            comment=unit.comment,
        )
        return pu
