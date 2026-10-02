from pydantic import BaseModel

from citadel.domain.unit.cardio import CardioUnit
from citadel.domain.unit.strength import LiftingUnit


class UnitLogResponse(BaseModel):
    status: str


LoadedUnits = list[CardioUnit] | list[LiftingUnit]
