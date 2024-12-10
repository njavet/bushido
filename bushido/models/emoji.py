from pydantic import BaseModel


class EmojiSpec(BaseModel):
    emoji_base: str
    emoji_ext: str | None
    name: str
    unit_name: str
    category: str

