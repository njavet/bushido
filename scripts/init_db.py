import csv
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido_server.conf import DB_URL
from bushido_server.persistence import SessionFactory
from bushido_server.persistence.models import Base, UnitCategoryTable, UnitSettingTable
from bushidolib.constants import UnitCategory


def upsert_categories(session: Session) -> dict[UnitCategory, UnitCategoryTable]:
    rows = {row.name: row for row in session.scalars(select(UnitCategoryTable)).all()}

    result: dict[UnitCategory, UnitCategoryTable] = {}

    for category in UnitCategory:
        row = rows.get(category.value)

        if row is None:
            row = UnitCategoryTable(name=category.value)
            session.add(row)
            session.flush()

        result[category] = row

    return result


def upsert_unit_settings(
    session: Session,
    categories: dict[UnitCategory, UnitCategoryTable],
    csv_path: Path,
) -> None:
    existing = {
        row.name: row for row in session.scalars(select(UnitSettingTable)).all()
    }

    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for record in reader:
            name = record["name"].strip()
            category = UnitCategory(record["category"].strip())

            category_row = categories[category]

            unit = existing.get(name)

            if unit is None:
                unit = UnitSettingTable(
                    name=name,
                    category_id=category_row.id,
                )
                session.add(unit)
                existing[name] = unit
            else:
                unit.category_id = category_row.id


def init_db(db_url: str = DB_URL) -> None:
    sf = SessionFactory(db_url)
    Base.metadata.create_all(bind=sf.engine)
    seed_file = Path(__file__).parent.parent / 'data' / 'units.csv'

    with sf.transaction() as session:
        categories = upsert_categories(session)
        upsert_unit_settings(session, categories, seed_file)


if __name__ == "__main__":
    init_db()
