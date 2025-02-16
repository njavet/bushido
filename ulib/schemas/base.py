from pydantic import BaseModel


class Category(BaseModel):
    name: str


class Emoji(BaseModel):
    base_emoji: str
    emoji: str
    unit_name: str
    category_name: str
    key: int


class Unit(BaseModel):
    timestamp: float
    fk_emoji: int

