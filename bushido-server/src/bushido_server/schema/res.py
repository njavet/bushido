from pydantic import BaseModel

from bushidolib.unit.cardio import CardioUnit
from bushidolib.unit.strength import LiftingUnit


class UnitLogResponse(BaseModel):
    status: str


LoadedUnits = list[CardioUnit] | list[LiftingUnit]
