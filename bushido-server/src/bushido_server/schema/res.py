from pydantic import BaseModel

from bushidolib.cardio import CardioUnit
from bushidolib.gym import GymUnit
from bushidolib.lifting import LiftingUnit
from bushidolib.wimhof import WimhofUnit


class UnitLogResponse(BaseModel):
    status: str


LoadedUnits = list[CardioUnit] | list[GymUnit] | list[LiftingUnit] | list[WimhofUnit]
