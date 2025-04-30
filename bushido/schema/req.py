from pydantic import BaseModel


class UnitLogRequest(BaseModel):
    text: str
