import collections

import helpers
# project imports
from db import Unit


class UnitModule(object):
    def __init__(self, subunit_model):
        self.subunit_model = subunit_model

    def retrieve_units(self, agent_id):
        query = (Unit
                 .select(Unit, self.subunit_model)
                 .where(Unit.agent == agent_id)
                 .join(self.subunit_model)
                 .order_by(Unit.unix_timestamp.desc()))
        return query

    def datetime2unit(self, user_id):
        query = self.retrieve_units(user_id)
        dt2unit = collections.defaultdict(list)
        for unit in query:
            dt = helpers.get_datetime_from_unix_timestamp(unit.unix_timestamp)
            dt2unit[dt].append(unit)
        return dt2unit

    def date2units(self, user_id):
        query = self.retrieve_units(user_id)
        date2units = collections.defaultdict(list)
        for unit in query:
            dt = helpers.get_datetime_from_unix_timestamp(unit.unix_timestamp)
            d = helpers.get_bushido_date_from_datetime(dt)
            date2units[d].append(unit)
        return date2units

