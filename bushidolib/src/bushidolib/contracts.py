from typing import Annotated

from pydantic import Field

from bushidolib.units.cardio import CardioUnit
from bushidolib.units.gym import GymUnit
from bushidolib.units.lifting import LiftingUnit
from bushidolib.wimhof import WimhofUnit

LoggedUnit = Annotated[
    CardioUnit | GymUnit | LiftingUnit | WimhofUnit,
    Field(discriminator="unit_category"),
]
