from typing import Optional
import collections
import importlib
import inspect
from dataclasses import dataclass
import logging

# project imports
import config
import db
import helpers
import exceptions


logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    success: bool
    msg: str


@dataclass
class UnitMessage:
    emoji_payload: str
    comment: str | None


class UnitManager:
    def __init__(self, emojis: dict) -> None:
        self.emoji2proc = {}
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

    def _load_emoji_dicts(self, module_name, module, emoji_uname_lst) -> None:
        for emoji, unit_name in emoji_uname_lst:
            self.emoji2proc[emoji] = module.UnitProcessor(module_name,
                                                          unit_name,
                                                          emoji)

    def _load_unit_modules(self, emojis):
        for module_name, emoji_uname_lst in self._parse_emoji_dix(emojis).items():
            module_path = '.'.join([config.unit_modules_dir, module_name])
            module = importlib.import_module(module_path)
            print('module', module_name)
            subunit_model = [member for member in inspect.getmembers(module)
                             if inspect.isclass(member[1])
                             and member[0] == module_name.capitalize()][0][1]
            self._load_emoji_dicts(module_name, module, emoji_uname_lst)
            # TODO fix this
            db.init_storage([subunit_model])

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

        try:
            self.unit_processor.parse_words(words)
        except exceptions.UnitProcessingError as err:
            return ProcessingResult(False, str(err))
        else:
            self.unit_message = UnitMessage(emoji_payload=' '.join([emoji] + words),
                                            comment=comment)
            return ProcessingResult(True, 'Unit confirmed!')

    def save_unit_data(self, tg_message_data):
        self.unit_processor.save_unit(tg_message_data)
        tg_message_data.set_data(self.unit_message.emoji_payload,
                                 self.unit_message.comment)
        self.unit_processor.save_unit_message(tg_message_data)

