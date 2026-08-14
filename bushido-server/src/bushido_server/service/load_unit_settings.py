from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido_server.persistence.models import UnitCategoryTable, UnitSettingTable
from bushidolib.constants import UnitCategory
from bushidolib.contracts.unit import UnitSetting


def load_unit_settings(session: Session) -> list[UnitSetting]:
    stmt = select(
        UnitSettingTable.name,
        UnitCategoryTable.name,
    ).join(
        UnitCategoryTable,
        UnitSettingTable.category_id == UnitCategoryTable.id,
    )

    result = session.scalars(stmt).all()
    return [UnitSetting(name=r.name, category=UnitCategory(r.category)) for r in result]
