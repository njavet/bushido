import datetime
from typing import Callable

from sqlalchemy.orm import Session

from bushido.db.repo import T_ORM, UnitRepo
from bushido.dtypes import T, UnitMapper, UnitRegistration
from bushido.units import Unit
from bushido.units.gym import GymData, gym_unit_settings
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
        # TODO repo per unit type
        unit_name = lifting_unit_settings[0].name
        return self._load_units(
            self.registry[unit_name].mapper,
            self.registry[unit_name].repo_factory,
            session,
            start_t=start_t,
            end_t=end_t,
        )

    def load_gym_units(
        self,
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[GymData]]:
        # TODO repo per unit type
        unit_name = gym_unit_settings[0].name
        return self._load_units(
            self.registry[unit_name].mapper,
            self.registry[unit_name].repo_factory,
            session,
            start_t=start_t,
            end_t=end_t,
        )

    @staticmethod
    def _load_units(
        mapper: UnitMapper[T, T_ORM],
        repo_factory: Callable[[Session], UnitRepo[T_ORM]],
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[T]]:
        units = repo_factory(session).fetch_units(start_t=start_t, end_t=end_t)
        parsed_units = [mapper.from_orm(unit) for unit in units]
        return parsed_units
