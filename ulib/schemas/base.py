# is it good practice to use the db key in the model ?
from pydantic import BaseModel


class Emoji(BaseModel):
    base_emoji: str
    emoji: str
    unit_name: str
    category_name: str
    key: int


class Unit(BaseModel):
    timestamp: float
    payload: str
    comment: str | None
    fk_emoji: int

