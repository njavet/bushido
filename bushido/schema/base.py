from pydantic import BaseModel


class UnitSpec(BaseModel):
    timestamp: int
    unit_name: str
    words: list[str]
    comment: str | None = None
