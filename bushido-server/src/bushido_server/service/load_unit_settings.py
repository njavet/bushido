from sqlalchemy.orm import Session

from bushidolib.unit import UnitSetting

from bushido_server.persistence.repos import load_unit_settings


def load_unit_mappings(session: Session) -> list[UnitSetting]:
    return load_unit_settings(session)
