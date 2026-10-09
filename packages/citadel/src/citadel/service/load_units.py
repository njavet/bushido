from sqlalchemy.orm import Session

from citadel.exceptions import UnitParsingError
from citadel.persistence.models import Spartan
from citadel.registry import UNIT_REGISTRY
from citadel.schema.req import LoadUnitRequest
from citadel.schema.res import LoggedUnit


def load_units(
    request: LoadUnitRequest, session: Session, spartan: Spartan
) -> list[LoggedUnit]:
    try:
        spec = UNIT_REGISTRY[request.unit_name]
    except KeyError as e:
        raise UnitParsingError(f"Unknown unit: {request.unit_name}") from e

    repo = spec.repo(session)
    return repo.fetch_units(
        spartan_id=spartan.id, start_t=request.start_t, end_t=request.end_t
    )
