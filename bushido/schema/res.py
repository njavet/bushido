from datetime import date
from pydantic import BaseModel

from bushido.data.base_models import MDEmojiModel


class MDEmoji(BaseModel):
    emoji: str
    unit_name: str


class MDCategory(BaseModel):
    name: str
    emojis: list[MDEmoji]


class UnitResponse(BaseModel):
    date: date
    hms: str
    emoji: str
    unit_name: str
    payload: str
