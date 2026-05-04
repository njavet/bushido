from ..dtypes import ParsedUnit
from .orm import WorkUnit
from .parser import WorkSpec


class WorkMapper:
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[WorkSpec]) -> WorkUnit:
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
        return unit

    @staticmethod
    def from_orm(orm_unit: WorkUnit) -> ParsedUnit[WorkSpec]:
        pu = ParsedUnit(
            name=orm_unit.name,
            data=WorkSpec(
                start_t=orm_unit.start_t,
                end_t=orm_unit.end_t,
                location=orm_unit.location,
                employer=orm_unit.employer,
                project=orm_unit.project,
            ),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
