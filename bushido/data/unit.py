from sqlalchemy.orm import Session
from sqlalchemy import select
from bushido.data.base_tables import UnitTable, MDEmojiTable


class UnitRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        stmt = (select(MDEmojiTable.emoji,
                       UnitTable.timestamp,
                       UnitTable.payload,
                       UnitTable.comment)
                .join(UnitTable, MDEmojiTable.key == UnitTable.fk_emoji))

        if unit_name:
            stmt = stmt.where(MDEmojiTable.unit_name == unit_name)
        if start_t:
            stmt = stmt.where(start_t.timestamp() <= UnitTable.timestamp)
        if end_t:
            stmt = stmt.where(UnitTable.timestamp <= end_t.timestamp())

        return self.session.execute(stmt).all()
