from pydantic import BaseModel


class TapeUnit(BaseModel):
    waist: float
    right_arm: float | None = None
    left_arm: float | None = None
    right_leg: float | None = None
    left_leg: float | None = None
    shoulders: float | None = None
    chest: float | None = None
