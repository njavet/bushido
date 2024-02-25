# general imports
import datetime
import collections
import importlib

# project imports
from utils import exceptions


class StringProcessor:
    def __init__(self, emojis):
        self.emojis = emojis
        self.unit_processors = {}

    def process_string(self, input_string, user_id, recv_time=None):
        emoji, payload, comment = self._parse_unit(input_string)
        module_name, unit_name = self._parse_names(self.emojis[emoji])
        ap = self._load_unit_processor(emoji, module_name)

        # module specific activity processing
        try:
            words = payload.split()
            ap.process_unit(user_id, emoji, words, recv_time, unit_name, comment)
        except exceptions.UnitProcessingError as e:
            return ProcessingResult(False, error=str(e))
        except exceptions.UnitProcessingWarning as e:
            return ProcessingResult(True, warning=str(e))
        else:
            return ProcessingResult(True)

    def _parse_unit(self, input_string):
        parts = input_string.split('//', 1)
        emoji_payload = parts[0]
        comment = parts[1] if len(parts) > 1 else None

        if not emoji_payload:
            raise exceptions.InvalidUnitError('Input is empty')

        emoji, payload = emoji_payload.split(maxsplit=1)

        if emoji not in self.emojis:
            raise exceptions.InvalidUnitError('Invalid emoji: {}'.format(emoji))

        return emoji, payload, comment

    @staticmethod
    def _parse_names(emoji_mapping):
        if '.' in emoji_mapping:
            module_name, unit_name = emoji_mapping.split('.')
        else:
            module_name, unit_name = emoji_mapping, None
        return module_name, unit_name

    def _load_unit_processor(self, emoji, name):
        if emoji not in self.unit_processors:
            module = importlib.import_module('units.' + name)
            self.unit_processors[emoji] = module.UnitProcessor()
        return self.unit_processors[emoji]


class ProcessingResult:
    def __init__(self, success, data=None, warning=None, error=None):
        self.success = success
        self.data = data
        self.warning = warning
        self.error = error


class UnitProcessor:
    def __init__(self):
        self.unit = None
        self.unit_model = None

    def process_unit(self, user_id, emoji, words,
                     recv_time=None,
                     unit_name=None,
                     comment=None):
        self.init_unit(user_id, emoji, unit_name, comment)
        self.unit.set_time(recv_time)
        self.parse_and_save(words)

    def init_unit(self, user_id, unit_emoji, unit_name=None, comment=None):
        self.unit = self.unit_model(user=user_id,
                                    unit_emoji=unit_emoji,
                                    comment=comment)
        if unit_name:
            self.unit.unit_name = unit_name

    def parse_and_save(self, words):
        self.unit.parse(words)
        self.unit.save()

    def post_saving(self, user_id):
        pass


class Unit:
    def __init__(self):
        self.unit_retriever = None
        self.unit_stats = None


class UnitRetriever:
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


class UnitStats:
    pass


