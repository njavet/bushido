import datetime

# is it good practice to use the db key in the model ?
from pydantic import BaseModel


class EmojiSpec(BaseModel):
    emoji: str
    emoji_text: str
    unit_name: str
    category_name: str
    key: int


class UnitSpec(BaseModel):
    timestamp: int
    category_name: str
    unit_name: str
    emoji: str
    payload: str
    comment: str | None = None
