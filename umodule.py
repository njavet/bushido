# general imports
import abc
import collections
import datetime

# project imports
from db import Unit


class UModule(object):
    def __init__(self, subunit_model, unit_names):
        self.subunit_model = subunit_model
        self.unit_names = unit_names

    def retrieve_units(self, user_id):
        query = (
            Unit.select(Unit, self.subunit_model)
            .where(Unit.user_id == user_id)
            .join(self.subunit_model)
            .order_by(Unit.log_time.desc())
        )
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


class UnitProcessor(abc.ABC):
    def __init__(self, module_name, unit_name, emoji):
        self.module_name = module_name
        self.unit_name = unit_name
        self.unit_emoji = emoji
        self.unit = None
        self.subunit = None

    def process_unit(
        self, user_id: int, words: list, recv_time: datetime.datetime, comment=None
    ) -> None:
        # init unit
        self.init_unit(user_id, comment, recv_time)

        # possible preparation
        self.pre_saving(user_id)

        # save unit and handle subunit
        self.unit.save()
        self.subunit_handler(words)

        # possible follow-ups
        self.post_saving(user_id)

    def init_unit(self, user_id, recv_time, comment=None):
        self.unit = Unit(
            user_id=user_id,
            module_name=self.module_name,
            unit_name=self.unit_name,
            unit_emoji=self.unit_emoji,
            log_time=recv_time,
            comment=comment,
        )

    @classmethod
    def parse_words(cls, words) -> dict:
        raise NotImplementedError

    def subunit_handler(self, words):
        raise NotImplementedError

    def pre_saving(self, user_id):
        pass

    def post_saving(self, user_id):
        pass
