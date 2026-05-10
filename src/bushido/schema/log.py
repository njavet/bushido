from pydantic import BaseModel

from bushido.settings import Category


class Log(BaseModel):
    category: Category
    name: str
    emoji: bytes
