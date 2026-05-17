import datetime

from sqlalchemy.orm import Session

from bushido.domain.dtypes import UnitRegistration
from bushido.domain.units import Unit
from bushido.domain.units.gym import GymData, gym_unit_settings
from bushido.domain.units.lifting import LiftingData, lifting_unit_settings


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
        # TODO repo per unit type
        unit_name = lifting_unit_settings[0].name
        repo_factory = self.registry[unit_name].repo_factory
        return repo_factory(session).fetch_units(start_t=start_t, end_t=end_t)

    def load_gym_units(
        self,
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[GymData]]:
        # TODO repo per unit type
        unit_name = gym_unit_settings[0].name
        repo_factory = self.registry[unit_name].repo_factory
        return repo_factory(session).fetch_units(start_t=start_t, end_t=end_t)
