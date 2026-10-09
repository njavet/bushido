import collections
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from citadel import constants
from citadel.exceptions import UnitParsingError
from citadel.persistence.models import Spartan
from citadel.registry import UNIT_REGISTRY
from citadel.schema.req import LoadUnitRequest
from citadel.schema.res import UnitsPerDay
from citadel.unit.parsing import get_bushido_date_from_datetime


def load_units(
    request: LoadUnitRequest, session: Session, spartan: Spartan
) -> list[UnitsPerDay]:
    try:
        spec = UNIT_REGISTRY[request.unit_name]
    except KeyError as e:
        raise UnitParsingError(f"Unknown unit: {request.unit_name}") from e

    repo = spec.repo(session)
    units = repo.fetch_units(
        spartan_id=spartan.id, start_t=request.start_t, end_t=request.end_t
    )

    res = collections.defaultdict(list)
    # TODO timezone
    for unit in units:
        day = get_bushido_date_from_datetime(
            unit.log_time,
            ZoneInfo("Europe/Zurich"),
            start_hour=constants.DAY_START_HOUR,
        )
        res[day].append(unit)

    return [UnitsPerDay(day=day, units=units) for day, units in res.items()]
