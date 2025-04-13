from typing import Callable

# project imports
from bushido.exceptions import ValidationError, UploadError
from bushido.schema.base import UnitSpec


class UnitProcessor:
    def __init__(self, dm):
        self.dm = dm

    def process_input(self, unit_spec: UnitSpec) -> str:
        try:
            keiko_orm = parse_unit(unit_spec.words)
        except ValidationError as err:
            return err.message

        try:
            self.dm.upload_unit(unit_spec, keiko_orm)
            return 'Unit Confirmed'
        except UploadError as err:
            return err.message

    def preprocess_input(self, text: str):
        parts = text.split('#', 1)
        emoji_payload = parts[0]
        if not emoji_payload:
            raise ValidationError('Empty payload')
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        all_words = emoji_payload.split()
        emoji = all_words[0]
        unit_name = self.dm.emoji_to_unit_name(emoji)
        if unit_name is None:
            raise ValidationError('Invalid emoji')
        words = all_words[1:]
        return unit_name, words, comment
