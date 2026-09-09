from pydantic import BaseModel

from bushidolib.category.cardio import CardioUnit
from bushidolib.category.gym import GymUnit
from bushidolib.category.lifting import LiftingUnit
from bushidolib.category.wimhof import WimhofUnit


class UnitLogResponse(BaseModel):
    status: str


LoadedUnits = list[CardioUnit] | list[GymUnit] | list[LiftingUnit] | list[WimhofUnit]
