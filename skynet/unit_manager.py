# general imports
import importlib

# project imports
from utils import exceptions
import config


class UnitManager:
    def __init__(self):
        self.emoji2proc = {}
        self.modname2stats = {}
        self.load_modules()

    def load_modules(self):
        for emoji, compound_name in config.emojis.items():
            module_name, unit_name = compound_name.split('.')
            module = importlib.import_module('units.' + module_name)
            self.emoji2proc[emoji] = module.UnitProcessor(module_name,
                                                          unit_name,
                                                          emoji)
            if module_name not in self.modname2stats.keys():
                self.modname2stats[module_name] = module.ModuleStats([unit_name])
            else:
                self.modname2stats[module_name].unit_names.append(unit_name)

    def process_string(self, input_string, user_id, recv_time=None):
        # input_string = <emoji> <payload> // <comment>
        parts = input_string.split('//', 1)
        emoji_payload = parts[0]
        comment = parts[1] if len(parts) > 1 else None

        if not emoji_payload:
            raise exceptions.InvalidUnitError('Input is empty')

        emoji, payload = emoji_payload.split(maxsplit=1)
        try:
            unit_processor = self.emoji2proc[emoji]
        except KeyError:
            raise exceptions.InvalidUnitError('Invalid emoji: {}'.format(emoji))

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
