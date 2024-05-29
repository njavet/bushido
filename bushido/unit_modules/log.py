from dataclasses import dataclass
import peewee as pw

# project imports
import unit_processing
import exceptions


class UnitProcessor(unit_processing.UnitProcessor):
    def __init__(self, module_name, unit_name, unit_emoji):
        super().__init__(module_name, unit_name, unit_emoji)

    def parse_words(self, words: list) -> None:
        try:
            log_str = words[0]
        except IndexError:
            raise exceptions.UnitProcessingError('empty log')

        self.attrs = Attrs(log_str=log_str)

    def save_subunit(self):
        Log.create(unit_id=self.unit,
                   log_str=self.attrs.log_str)


@dataclass
class Attrs(unit_processing.Attrs):
    log_str: str


class Log(unit_processing.SubUnit):
    log_str = pw.CharField()
