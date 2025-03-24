import datetime
from zoneinfo import ZoneInfo
from abc import ABC

# project imports
from bushido.model.base import UnitSpec


class InputProcessor:
    def __init__(self, emoji2processor):
        self.emoji2processor = emoji2processor

    def load_processors(self):
        pass

    def process_input(self, text):
        try:
            emoji, words, comment = self.preprocess_input(text)
        except ValueError as err:
            return str(err)

        try:
            processor = self.emoji2processor[emoji]
        except KeyError:
            return 'Unknown Emoji'

        try:
            processor.process_unit(emoji, words, comment)
            return 'Unit Confirmed'
        except ValueError as err:
            return str(err)

    @staticmethod
    def preprocess_input(text: str):
        parts = text.split('//', 1)
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


class AbsUnitProcessor(ABC):
    def __init__(self, engine):
        self.parser = None
        self.uploader = None

    def process_unit(self, emoji, words, comment):
        unit_spec = self.create_unit_spec(emoji, words, comment)
        keiko_spec = self.parser.parse_unit(words)
        self.uploader(unit_spec, keiko_spec)

    @staticmethod
    def create_unit_spec(emoji, words, comment):
        now = datetime.datetime.now().replace(tzinfo=ZoneInfo('Europe/Zurich'))
        timestamp = int(now.timestamp())
        unit_spec = UnitSpec(timestamp=timestamp,
                             emoji=emoji,
                             payload=' '.join(words),
                             comment=comment)
        return unit_spec


class AbsUnitParser(ABC):
    def __init__(self):
        pass

    def parse_unit(self, words):
        raise NotImplementedError

