# is it good practice to use the db key in the model ?
from pydantic import BaseModel


class UnitSpec(BaseModel):
    timestamp: int
    unit_name: str
    payload: str
    comment: str | None = None
