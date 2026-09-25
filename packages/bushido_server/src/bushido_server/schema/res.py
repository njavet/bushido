from bushidolib.unit.cardio import CardioUnit
from bushidolib.unit.strength import LiftingUnit
from pydantic import BaseModel


class UnitLogResponse(BaseModel):
    status: str


LoadedUnits = list[CardioUnit] | list[LiftingUnit]
