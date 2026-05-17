import datetime
from typing import Callable, TypeVar

from sqlalchemy.orm import Session

from bushido.db.model.base import UnitTable
from bushido.db.repo import UnitRepo
from bushido.dtypes import UnitRegistration
from bushido.protocols import UnitMapper
from bushido.units import Unit
from bushido.units.gym import GymData
from bushido.units.lifting import LiftingData, lifting_unit_settings

T = TypeVar("T")
TU = TypeVar("TU", bound=UnitTable)


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
        unit_name = lifting_unit_settings[0].name
        units = (
            self.registry[unit_name]
            .repo(session)
            .fetch_units(start_t=start_t, end_t=end_t)
        )
        parsed_units = [
            self.registry[unit_name].mapper.from_orm(unit) for unit in units
        ]
        return parsed_units

    @staticmethod
    def _load_units(
        mapper: UnitMapper[T, TU],
        repo_factory: Callable[[Session], UnitRepo[TU]],
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[T]]:
        units = repo_factory(session).fetch_units(start_t=start_t, end_t=end_t)
        parsed_units = [mapper.from_orm(unit) for unit in units]
        return parsed_units
