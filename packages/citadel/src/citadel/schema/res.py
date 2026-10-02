from citadel.domain.unit.cardio import CardioUnit
from citadel.domain.unit.strength import LiftingUnit
from pydantic import BaseModel


class UnitLogResponse(BaseModel):
    status: str


LoadedUnits = list[CardioUnit] | list[LiftingUnit]
