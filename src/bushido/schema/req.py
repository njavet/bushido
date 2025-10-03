from pydantic import BaseModel


class UnitLogRequest(BaseModel):
    line: str
