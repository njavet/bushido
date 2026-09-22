from pydantic import BaseModel

from bushidolib.unit.cardio import CardioUnit
from bushidolib.category.martial_arts import GymUnit
from bushidolib.category.strength import LiftingUnit
from bushidolib.category.wimhof import WimhofUnit


class UnitLogResponse(BaseModel):
    status: str


LoadedUnits = list[CardioUnit] | list[GymUnit] | list[LiftingUnit] | list[WimhofUnit]
