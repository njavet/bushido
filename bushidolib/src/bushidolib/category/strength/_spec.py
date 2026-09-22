from pydantic import BaseModel

from bushidolib.schema.unit import BaseUnit


class LiftingSetData(BaseModel):
    set_nr: int
    weight: float
    reps: float
    rest: float


class LiftingData(BaseModel):
    sets: list[LiftingSetData]
    variant: str | None = None


class LiftingUnit(BaseUnit, LiftingData):
    pass


class StrengthUnit(BaseUnit):
    pass
