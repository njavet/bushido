
# project imports
from ulib.db import DatabaseManager
from ulib.parsers.gym import GymParser
from ulib.parsers.lifting import LiftingParser


class UnitManager:
    def __init__(self) -> None:
        self.dbm = DatabaseManager('sqlite.db')
        self.parsers = self.load_parsers()

    @staticmethod
    def load_parsers():
        parsers = {'gym': GymParser(),
                   'lifting': LiftingParser()}
        return parsers


    def process_input(self, unix_timestamp, input_str):
        try:
            emoji, words, comment = self._preprocess_string(input_str)
        except ValueError as err:
            return str(err)

        try:
            emoji_spec = self.dbm.emoji_dix[emoji]
        except KeyError:
            return 'Unknown emoji'

        try:
            attrs = self.parsers[emoji_spec.category].parse_words(words)
        except ValueError:
            return 'parsing error'

        self.dbm.uploaders[emoji_spec.category].upload_unit(
            unix_timestamp, emoji_spec.key, ' '.join(words), comment, attrs
        )

    @staticmethod
    def _preprocess_string(input_str: str):
        parts = input_str.split('//', 1)
        emoji_payload = parts[0]
        if not emoji_payload:
            raise ValueError('Empty payload')
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        all_words = emoji_payload.split()
        emoji = all_words[0]
        words = all_words[1:]
        return emoji, words, comment
