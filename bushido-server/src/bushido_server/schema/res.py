from typing import Annotated

from pydantic import BaseModel, Field

from bushidolib.cardio import CardioUnit
from bushidolib.gym import GymUnit
from bushidolib.lifting import LiftingUnit
from bushidolib.wimhof import WimhofUnit


class UnitLogResponse(BaseModel):
    status: str


LoadedUnits = list[CardioUnit] | list[GymUnit] | list[LiftingUnit] | list[WimhofUnit]
LoggedUnit = Annotated[
    CardioUnit | GymUnit | LiftingUnit | WimhofUnit,
    Field(discriminator="unit_category"),
]
