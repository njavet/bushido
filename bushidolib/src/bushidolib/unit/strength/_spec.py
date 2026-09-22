from pydantic import BaseModel

from bushidolib.unit.base import BaseUnit, SpaceTimeData


class LiftingSetData(BaseModel):
    set_nr: int
    weight: float
    reps: float
    rest: float


class LiftingData(BaseModel):
    sets: list[LiftingSetData]
    variant: str = 'default'


class LiftingUnit(BaseUnit, LiftingData):
    exercise: str


class StrengthUnit(BaseUnit, SpaceTimeData):
    pass
