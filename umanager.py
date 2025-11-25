# general imports
import datetime
import importlib
import inspect

import peewee as pw

import config
import db

# project imports
import umodule
from utils import exceptions, utilities


class UManager:
    def __init__(self):
        self.emoji2proc = {}
        self.umodules = {}
        self.load_modules()
        self.create_tables()

    def create_tables(self):
        database = pw.SqliteDatabase(config.db_name)
        database.connect()
        ts = [m.subunit_model for m in self.umodules.values()]
        database.create_tables(ts, safe=True)
        database.close()

    def load_modules(self):
        for module_name, unit_lst in utilities.parse_module_dix().items():
            module = importlib.import_module("umodules." + module_name)
            subunit_model = [
                member
                for member in inspect.getmembers(module)
                if inspect.isclass(member[1]) and member[0] == module_name.capitalize()
            ][0][1]
            unit_names = []
            for emoji, unit_name in unit_lst:
                unit_names.append(unit_name)
                self.emoji2proc[emoji] = module.UnitProcessor(
                    module_name, unit_name, emoji
                )
            self.umodules[module_name] = umodule.UModule(subunit_model, unit_names)

    def process_string(self, input_string, user_id, recv_time=None):
        # input_string = <emoji> <payload> // <comment>
        parts = input_string.split("//", 1)
        emoji_payload = parts[0]
        comment = parts[1] if len(parts) > 1 else None

        if recv_time is None:
            recv_time = datetime.datetime.now()

        if not emoji_payload:
            raise exceptions.InvalidUnitError("Input is empty")

        try:
            emoji, payload = emoji_payload.split(maxsplit=1)
        except ValueError:
            raise exceptions.InvalidUnitError("Input is empty")

        try:
            unit_processor = self.emoji2proc[emoji]
        except KeyError:
            raise exceptions.InvalidUnitError("Invalid emoji: {}".format(emoji))

        db.Message.create(
            user_id=user_id, msg=emoji_payload, log_time=recv_time, comment=comment
        )

        try:
            words = payload.split()
            unit_processor.process_unit(user_id, words, comment, recv_time)
        except exceptions.UnitProcessingError as e:
            return ProcessingResult(False, error=str(e))
        except exceptions.UnitProcessingWarning as e:
            return ProcessingResult(True, warning=str(e))
        else:
            return ProcessingResult(True)


class ProcessingResult:
    def __init__(self, success, data=None, warning=None, error=None):
        self.success = success
        self.data = data
        self.warning = warning
        self.error = error
