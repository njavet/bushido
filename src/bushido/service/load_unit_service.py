import datetime

from sqlalchemy.orm import Session

from bushido.dtypes import UnitRegistration
from bushido.units import Unit
from bushido.units.lifting import LiftingData, lifting_unit_settings


class LoadUnitService:
    def __init__(
        self,
        registry: dict[str, UnitRegistration],
    ) -> None:
        self.registry = registry

    def load_lifting_units(
        self,
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[LiftingData]]:
        unit_name = lifting_unit_settings[0].unit_name
        units = (
            self.registry[unit_name]
            .repo(session)
            .fetch_units(start_t=start_t, end_t=end_t)
        )
        parsed_units = [
            self.registry[unit_name].mapper.from_orm(unit) for unit in units
        ]
        return parsed_units
