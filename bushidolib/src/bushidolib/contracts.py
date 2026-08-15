from typing import Annotated

from pydantic import Field

from bushidolib.cardio import CardioUnit
from bushidolib.gym import GymUnit
from bushidolib.lifting import LiftingUnit
from bushidolib.wimhof import WimhofUnit

LoggedUnit = Annotated[
    CardioUnit | GymUnit | LiftingUnit | WimhofUnit,
    Field(discriminator="unit_category"),
]
