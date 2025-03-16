from sqlalchemy import select
from sqlalchemy.orm import Session

# project imports
from bushido.db.base_tables import MDEmojiTable, UnitTable


class DisplayService:
    def __init__(self, dbm):
        self.dbm = dbm

    def get_units(self):
        stmt = (select(MDEmojiTable.base_emoji,
                       MDEmojiTable.ext_emoji,
                       UnitTable.timestamp,
                       UnitTable.payload)
                .join(UnitTable)
                ).order_by(UnitTable.timestamp)
        with Session(self.dbm.engine) as session:
            result = session.execute(stmt).all()

        return result



