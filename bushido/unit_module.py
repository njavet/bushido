import collections

# project imports
from db import Unit


class UnitModule(object):
    def __init__(self, subunit_model):
        self.subunit_model = subunit_model

    def retrieve_units(self, agent_id):
        query = (Unit
                 .select(Unit, self.subunit_model)
                 .where(Unit.agent_id == agent_id)
                 .join(self.subunit_model)
                 .order_by(Unit.log_time.desc()))
        return query

    def datetime2unit(self, user_id):
        query = self.retrieve_units(user_id)
        dt2unit = collections.defaultdict(list)
        for unit in query:
            dt2unit[unit.log_time].append(unit)
        return dt2unit

    def date2units(self, user_id):
        query = self.retrieve_units(user_id)
        date2units = collections.defaultdict(list)
        for unit in query:
            date2units[unit.log_date].append(unit)
        return date2units

