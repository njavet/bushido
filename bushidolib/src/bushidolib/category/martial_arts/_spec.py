import datetime

from pydantic import BaseModel

from bushidolib.schema.unit import BaseUnit


class GymData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str


class GymUnit(BaseUnit, GymData):
    pass
