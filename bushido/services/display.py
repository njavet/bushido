import pytz
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

# project imports
from bushido.db.base_tables import MDEmojiTable, UnitTable
from bushido.schemas.base import UnitDisplay
from bushido.utils.emojis import combine_emoji


class DisplayService:
    def __init__(self, dbm):
        self.dbm = dbm

    def get_units(self):
        stmt = (select(MDEmojiTable.base_emoji,
                       MDEmojiTable.ext_emoji,
                       UnitTable.timestamp,
                       UnitTable.payload,
                       UnitTable.comment)
                .join(UnitTable)
                ).order_by(UnitTable.timestamp)
        with Session(self.dbm.engine) as session:
            result = session.execute(stmt).all()
        lst = []
        zurich = pytz.timezone('Europe/Zurich')
        for unit in result:
            dt_utc = datetime.fromtimestamp(unit.timestamp, tz=pytz.utc)
            ud = UnitDisplay(dt=dt_utc.astimezone(zurich),
                             emoji=combine_emoji(unit.base_emoji, unit.ext_emoji),
                             payload=unit.payload,
                             comment=unit.comment)
            lst.append(ud)

        return lst



