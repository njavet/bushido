import datetime

# is it good practice to use the db key in the model ?
from pydantic import BaseModel


class EmojiSpec(BaseModel):
    emoji_base: str
    emoji_ext: str | None
    unit_name: str
    category_name: str
    key: int


class UnitSpec(BaseModel):
    timestamp: int
    emoji: str
    payload: str
    comment: str | None = None
