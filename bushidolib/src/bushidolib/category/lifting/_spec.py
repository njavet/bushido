from pydantic import BaseModel

from ..base import BaseUnit


class LiftingSetData(BaseModel):
    set_nr: int
    weight: float
    reps: float
    rest: float


class LiftingData(BaseModel):
    sets: list[LiftingSetData]
    variant: str | None = None


class LiftingUnit(BaseUnit):
    sets: list[LiftingSetData]
    variant: str | None = None
