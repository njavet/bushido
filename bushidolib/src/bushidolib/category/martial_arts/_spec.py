import datetime

from pydantic import BaseModel

from bushidolib.schema.unit import BaseUnit, SpaceTimeData


class MartialArtsUnit(BaseUnit, SpaceTimeData):
    pass
