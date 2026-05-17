from pydantic import BaseModel


class UnitLogRequest(BaseModel):
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None
