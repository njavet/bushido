from pydantic import BaseModel


class MDCategory(BaseModel):
    name: str


class MDEmoji(BaseModel):
    emoji_base: str
    emoji_ext: str | None
    emoji_name: str
    unit_name: str
    fk_category: int


class