from collections import defaultdict
from bushido.data.base_repo import BaseRepository
from bushido.utils.dt_functions import (get_datetime_from_timestamp,
                                        get_bushido_date_from_datetime)


class UnitService:
    def __init__(self, base_repo: BaseRepository):
        self.repo = base_repo

    @classmethod
    def from_session(cls, session):
        return cls(BaseRepository(session))

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        units = self.repo.get_units(unit_name, start_t, end_t)
        dix = defaultdict(list)
        for unit in units:
            dt = get_datetime_from_timestamp(unit.timestamp)
            bushido_dt = get_bushido_date_from_datetime(dt)
            hms = dt.strftime('%H:%M')
            dix[bushido_dt].append((hms, unit.emoji, unit.payload))
        return dix
