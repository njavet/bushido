from abc import ABC, abstractmethod
import datetime
from bushido.conf import LOCAL_TIME_ZONE
from bushido.utils.parsing import parse_option
from bushido.data.base_models import UnitModel
from bushido.data.base_repo import BaseRepository


class UnitService:
    def __init__(self, base_repo: BaseRepository):
        self.repo = base_repo

    @classmethod
    def from_session(cls, session):
        return cls(BaseRepository(session))

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        return self.repo.get_units(unit_name, start_t, end_t)
