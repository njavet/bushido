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



