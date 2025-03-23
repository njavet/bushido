from pydantic import BaseModel

# project imports


class GymUnit(BaseModel):
    emoji: str
    start_t: int
    end_t: int
    gym: str
    comment: str | None = None
