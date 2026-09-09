from typing import Annotated

from pydantic import Field

from bushidolib.category.cardio import CardioUnit
from bushidolib.category.gym import GymUnit
from bushidolib.category.lifting import LiftingUnit
from bushidolib.category.wimhof import WimhofUnit

LoggedUnit = Annotated[
    CardioUnit | GymUnit | LiftingUnit | WimhofUnit,
    Field(discriminator="unit_category"),
]
