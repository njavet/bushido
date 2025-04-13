from pydantic import BaseModel


class KeikoSpec(BaseModel):
    weight: float
    belly: float | None
