import datetime
from typing import Callable

from sqlalchemy.orm import Session

from bushido.domain.dtypes import T_DOMAIN, UnitRegistration, UnitRepo
from bushido.domain.units import (
    GymData,
    LiftingData,
    Unit,
    gym_unit_settings,
    lifting_unit_settings,
)


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
            self.registry[unit_name].repo_factory,
            session,
            start_t=start_t,
            end_t=end_t,
        )

    @staticmethod
    def _load_units(
        repo_factory: Callable[[Session], UnitRepo[T_DOMAIN]],
        session: Session,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[T_DOMAIN]]:
        return repo_factory(session).fetch_units(start_t=start_t, end_t=end_t)
