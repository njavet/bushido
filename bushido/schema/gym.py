from pydantic import BaseModel

# project imports


class KeikoSpec(BaseModel):
    start_t: int
    end_t: int
    gym: str
