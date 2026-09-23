from bushidolib.category.wimhof import WimhofUnit
from pydantic import BaseModel

from bushidolib.unit.cardio import CardioUnit
from bushidolib.unit.martial_arts import GymUnit
from bushidolib.unit.strength import LiftingUnit


class UnitLogResponse(BaseModel):
    status: str


LoadedUnits = list[CardioUnit] | list[GymUnit] | list[LiftingUnit] | list[WimhofUnit]
