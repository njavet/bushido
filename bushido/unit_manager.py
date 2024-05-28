from typing import Optional
import datetime
import collections
import importlib
import inspect
from dataclasses import dataclass
import logging

# project imports
from unit_module import UnitModule
import config
import helpers
import exceptions
import parsing


logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    success: bool
    msg: str


@dataclass
class UnitMessage:
    from_id: int
    to_id: int
    log_time: datetime.datetime
    unix_timestamp: float


class UnitManager:
    def __init__(self, emojis: dict) -> None:
        self.emoji2proc = {}
        self.unit_modules = {}
        self._load_unit_modules(emojis)
        # TODO temporary unit storage data, check if this is good practice
        self.unit_processor = None
        self.unit_message: UnitMessage | None = None

    @staticmethod
    def _parse_emoji_dix(emojis: dict) -> dict:
        """
        emojis dict will be parsed to a dict of the format:
        module_name -> [(emoji, unit_name), ...]

        :param emojis:
        :return:
        """
        dix = collections.defaultdict(list)
        for emoji, compound_name in emojis.items():
            module_name, unit_name = compound_name.split('.')
            dix[module_name].append((emoji, unit_name))
        return dix

    def _load_unit_processors(self, module_name, module, emoji_uname_lst) -> None:
        for emoji, unit_name in emoji_uname_lst:
            self.emoji2proc[emoji] = module.UnitProcessor(module_name,
                                                          unit_name,
                                                          emoji)

    def _load_unit_modules(self, emojis):
        for module_name, emoji_uname_lst in self._parse_emoji_dix(emojis).items():
            module_path = '.'.join([config.unit_modules_dir, module_name])
            module = importlib.import_module(module_path)
            subunit_model = [member for member in inspect.getmembers(module)
                             if inspect.isclass(member[1])
                             and member[0] == module_name.capitalize()][0][1]
            self._load_unit_processors(module_name, module, emoji_uname_lst)
            self.unit_modules[module_name] = UnitModule(subunit_model)

    @staticmethod
    def _preprocess_string(input_string) -> Optional[tuple[str, list, str | None]]:
        # input_string = <emoji> <payload> // <comment>
        parts = input_string.split('//', 1)
        emoji_payload = parts[0]
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None

        if not emoji_payload:
            raise exceptions.UnitProcessingError('Empty payload')

        all_words = emoji_payload.split()
        emoji = helpers.convert_emoji(all_words[0])
        words = all_words[1:]
        return emoji, words, comment

    def process_string(self, input_string) -> ProcessingResult:
        try:
            emoji, words, comment = self._preprocess_string(input_string)
        except exceptions.UnitProcessingError as err:
            return ProcessingResult(False, str(err))

        try:
            self.unit_processor = self.emoji2proc[emoji]
        except KeyError:
            return ProcessingResult(False, f'Invalid emoji: {emoji}')

        # local time string
        dt_str = parsing.parse_option(words, '-dt')
        if dt_str:
            self.unit_processor.unix_timestamp = helpers.convert_local_dt_to_unix_timestamp(dt_str)
        else:
            self.unit_processor.unix_timestamp = None

        try:
            self.unit_processor.parse_words(words)
        except exceptions.UnitProcessingError as err:
            return ProcessingResult(False, str(err))
        else:
            # TODO fix this
            self.unit_processor.payload = ' '.join(words)
            self.unit_processor.comment = comment
            return ProcessingResult(True, 'Unit confirmed!')

    def save_unit_data(self, agent_id, unix_timestamp):
        # unix_timestamp might be different for unit and message, because
        #  of -dt
        if self.unit_processor.unix_timestamp is None:
            self.unit_processor.unix_timestamp = unix_timestamp
        self.unit_processor.save_unit(agent_id)
        self.unit_processor.save_unit_message(unix_timestamp)

