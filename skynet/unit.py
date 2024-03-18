# general imports
import collections
import abc

# project imports
import db


class UnitProcessor(abc.ABC):
    def __init__(self, module_name, unit_name, emoji):
        self.module_name = module_name
        self.unit_name = unit_name
        self.unit_emoji = emoji
        self.unit = None
        self.subunit = None

    def process_unit(self,
                     user_id: int,
                     words: list,
                     comment=None,
                     recv_time=None):
        # init unit
        self.init_unit(user_id, comment)
        self.unit.set_time(recv_time)

        # possible preparation
        self.pre_saving(user_id)

        # save unit and handle subunit
        self.unit.save()
        self.subunit_handler(words)

        # possible follow-ups
        self.post_saving(user_id)

    def init_unit(self, user_id, comment=None):
        self.unit = db.Unit(user_id=user_id,
                            module_name=self.module_name,
                            unit_name=self.unit_name,
                            unit_emoji=self.unit_emoji,
                            comment=comment)

    @classmethod
    def parse_words(cls, words) -> dict:
        raise NotImplementedError

    def subunit_handler(self, words):
        raise NotImplementedError

    def pre_saving(self, user_id):
        pass

    def post_saving(self, user_id):
        pass


class ModuleStats(abc.ABC):
    def __init__(self, unit_names):
        self.unit_names = unit_names
        self.subunit_model = None

    def retrieve_units(self, user_id):
        query = (db.Unit
                 .select(db.Unit, self.subunit_model)
                 .where(db.Unit.user_id == user_id)
                 .join(self.subunit_model)
                 .order_by(db.Unit.log_time.desc()))

        return query

    def datetime2unit(self, user_id):
        # TODO rename method
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

    def date2unit_str(self, user_id):
        raise NotImplementedError

    def unit_name2unit_list(self, user_id):
        raise NotImplementedError
