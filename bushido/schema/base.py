from pydantic import BaseModel


class EmojiSpec(BaseModel):
    emoji: str
    unit_name: str


class UnitSpec(BaseModel):
    unit_name: str
    words: list[str]
    comment: str | None = None
