from pydantic import BaseModel


class Category(BaseModel):
    name: str


class Emoji(BaseModel):
    emoji_base: str
    emoji_ext: str | None
    emoji_name: str
    unit_name: str
    fk_category: int


class Unit(BaseModel):
    timestamp: float
    fk_emoji: int

