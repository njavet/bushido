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
    dt: datetime.datetime
    emoji: str
    payload: str
    comment: str | None
