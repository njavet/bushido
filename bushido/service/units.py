from typing import Callable
import datetime
from zoneinfo import ZoneInfo

# project imports
from bushido.exceptions import ValidationError, UploadError
from bushido.schema.base import UnitSpec


class UnitProcessor:
    def __init__(self, dm):
        self.dm = dm

    def process_input(self,
                      text: str,
                      parse_unit: Callable,
                      create_keiko_orm: Callable) -> str:
        try:
            emoji, words, comment = self.preprocess_input(text)
        except ValidationError as err:
            return err.message

        unit_name = self.dm.emoji_to_unit_name(emoji)
        if unit_name is None:
            return 'Invalid emoji'

        try:
            unit_spec = self.create_unit_spec(unit_name, words, comment)
            keiko_spec = parse_unit(words)
        except ValidationError as err:
            return err.message

        try:
            keiko_orm = create_keiko_orm(keiko_spec)
            self.dm.upload_unit(unit_spec, keiko_orm)
            return 'Unit Confirmed'
        except UploadError as err:
            return err.message

    @staticmethod
    def preprocess_input(text: str):
        parts = text.split('//', 1)
        emoji_payload = parts[0]
        if not emoji_payload:
            raise ValidationError('Empty payload')
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        all_words = emoji_payload.split()
        emoji = all_words[0]
        words = all_words[1:]
        return emoji, words, comment

    @staticmethod
    def create_unit_spec(unit_name, words, comment):
        now = datetime.datetime.now().replace(tzinfo=ZoneInfo('Europe/Zurich'))
        timestamp = int(now.timestamp())
        unit_spec = UnitSpec(timestamp=timestamp,
                             unit_name=unit_name,
                             payload=' '.join(words),
                             comment=comment)
        return unit_spec
