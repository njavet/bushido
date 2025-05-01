from collections import defaultdict

# project imports
from bushido.schema.res import UnitResponse, MDResponse
from bushido.utils.dtf import create_unit_response_dt
from bushido.data.repo import Repository


class BaseUnitService:
    def __init__(self, repo: Repository):
        self.repo = repo

    @classmethod
    def from_session(cls, session):
        return cls(Repository(session))

    def get_master_data(self):
        data = self.repo.get_master_data()
        dix = defaultdict(list)
        for cat, emoji, unit_name in data:
            dix[cat].append((emoji, unit_name))
        return MDResponse(categories=dix)

    def get_emoji_for_unit(self, unit_name):
        emoji = self.repo.get_emoji_for_unit(unit_name)
        return emoji

    def get_units(self,
                  category=None,
                  unit_name=None,
                  start_t=None,
                  end_t=None) -> list[UnitResponse]:
        units = self.repo.get_units(category,
                                    unit_name,
                                    start_t,
                                    end_t)
        unit_lst = []
        for unit in units:
            bushido_date, hms = create_unit_response_dt(unit.timestamp)
            ur = UnitResponse(date=bushido_date,
                              hms=hms,
                              emoji=unit.emoji,
                              unit_name=unit.unit_name,
                              payload=unit.payload)
            unit_lst.append(ur)
        return unit_lst

    def get_units_by_day(self,
                         category=None,
                         unit_name=None,
                         start_t=None,
                         end_t=None) -> dict:
        units = self.get_units(category, unit_name, start_t, end_t)
        dix = defaultdict(list)
        for unit in units:
            dix[unit.date].append(unit)
        return dix
