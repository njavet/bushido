from pydantic import BaseModel


class UnitLogResponse(BaseModel):
    status: str
