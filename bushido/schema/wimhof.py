from pydantic import BaseModel


class KeikoSpec(BaseModel):
    weights: list[float]
    reps: list[float]
    pauses: list[float]
