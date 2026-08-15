import datetime

from pydantic import BaseModel

from bushidolib.constants import UnitCategory


class LoadUnitRequest(BaseModel):
    unit_category: UnitCategory
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None
