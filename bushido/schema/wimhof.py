from pydantic import BaseModel


class KeikoSpec(BaseModel):
    breaths: list[float]
    retentions: list[float]
