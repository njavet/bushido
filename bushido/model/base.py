import datetime

# is it good practice to use the db key in the model ?
from pydantic import BaseModel


class EmojiProcessor(BaseModel):
    base_emoji: str
    emoji: str
    unit_name: str
    category_name: str
    key: int


class UnitDisplay(BaseModel):
    bushido_date: datetime.date
    day_time: datetime.time
    emoji: str
    payload: str
    comment: str | None
