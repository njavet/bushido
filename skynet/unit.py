# general imports
import collections
import abc


class UnitProcessor(abc.ABC):
    def __init__(self, unit_emoji, unit_name=None):
        self.unit_emoji = unit_emoji
        self.unit_name = unit_name
        self.unit = None
        self.unit_model = None
        self.subunit_model = None

    def process_unit(self,
                     user_id: int,
                     words: list,
                     comment=None,
                     recv_time=None):
        self.init_unit(user_id, comment)
        self.unit.set_time(recv_time)
        self.parse_and_save(words)
        self.post_saving(user_id)

    def init_unit(self, user_id, comment=None):
        self.unit = self.unit_model(user=user_id,
                                    unit_emoji=self.unit_emoji,
                                    comment=comment)
        if self.unit_name:
            self.unit.unit_name = self.unit_name

    def parse_and_save(self, words):
        self.unit.parse(words)
        self.unit.save()

    def post_saving(self, user_id):
        pass


class UnitStats(abc.ABC):
    def __init__(self):
        self.unit_model = None
        self.subunit_model = None

    def retrieve_units(self, user_id):
        if self.subunit_model:
            query = (self.unit_model
                     .select(self.unit_model, self.subunit_model)
                     .where(self.unit_model.user == user_id)
                     .join(self.subunit_model)
                     .order_by(self.unit_model.log_time.desc()))
        else:
            query = (self.unit_model
                     .select()
                     .where(self.unit_model.user == user_id)
                     .order_by(self.unit_model.log_time.desc()))

        return query

    def datetime2unit(self, user_id):
        # TODO rename method
        query = self.retrieve_units(user_id)
        if self.subunit_model:
            dt2unit = collections.defaultdict(list)
            for unit in query:
                dt2unit[unit.log_time].append(unit)
        else:
            dt2unit = {unit.log_time: unit for unit in query}
        return dt2unit

    def date2units(self, user_id):
        query = self.retrieve_units(user_id)
        date2units = collections.defaultdict(list)
        for unit in query:
            date2units[unit.log_date].append(unit)
        return date2units

    def date2unit_str(self, user_id):
        raise NotImplementedError
