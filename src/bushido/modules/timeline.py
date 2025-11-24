from typing import Any

from sqlalchemy.orm import Session

from bushido.modules.dtypes import DisplayUnit
from bushido.modules.gym import GymUnit, format_gym_unit
from bushido.modules.lifting import LiftingSet, LiftingUnit, format_lifting_unit
from bushido.modules.repo import UnitRepo
from bushido.modules.wimhof import WimhofRound, WimhofUnit, format_wimhof_unit


def fetch_display_units(session: Session) -> list[DisplayUnit]:
    gym_repo = UnitRepo[GymUnit, Any](session=session, unit_cls=GymUnit)
    lifting_repo = UnitRepo[LiftingUnit, LiftingSet](
        session=session, unit_cls=LiftingUnit, subrels=LiftingUnit.subunits
    )
    wimhof_repo = UnitRepo[WimhofUnit, WimhofRound](
        session=session, unit_cls=WimhofUnit, subrels=WimhofUnit.subunits
    )

    gyms = [
        DisplayUnit(
            name=u.name,
            log_time=u.log_time,
            payload=format_gym_unit(u),
        )
        for u in gym_repo.fetch_units()
    ]
    liftings = [
        DisplayUnit(
            name=u.name,
            log_time=u.log_time,
            payload=format_lifting_unit(u),
        )
        for u in lifting_repo.fetch_units()
    ]
    wimhofs = [
        DisplayUnit(
            name=u.name,
            log_time=u.log_time,
            payload=format_wimhof_unit(u),
        )
        for u in wimhof_repo.fetch_units()
    ]

    result = gyms + liftings + wimhofs
    result.sort(key=lambda du: du.log_time)
    return result
