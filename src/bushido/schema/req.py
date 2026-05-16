from pydantic import BaseModel


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None
