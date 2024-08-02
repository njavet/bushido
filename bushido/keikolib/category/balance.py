from dataclasses import dataclass, field
import peewee as pw

# project imports
from keikolib.abscat import Keiko, AbsProcessor, AbsRetriever, AbsUmojis


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    @dataclass
    class Attrs:
        weight: float
        fat: float | None = field(init=False)
        water: float | None = field(init=False)
        muscles: float | None = field(init=False)

        def set_optional_data(self, fat, water, muscles):
            self.fat = fat
            self.water = water
            self.muscles = muscles

    def _process_words(self, words: list) -> None:
        try:
            self.attrs = self.Attrs(weight=float(words[0]))
        except (IndexError, ValueError):
            raise ValueError('Specify the weight')

        try:
            fat = float(words[1])
        except (IndexError, ValueError):
            fat = None

        try:
            water = float(words[2])
        except (IndexError, ValueError):
            water = None

        try:
            muscles = float(words[3])
        except (IndexError, ValueError):
            muscles = None

        self.attrs.set_optional_data(fat, water, muscles)

    def _save_keiko(self, unit):
        Balance.create(unit_id=unit,
                       weight=self.attrs.weight,
                       fat=self.attrs.fat,
                       water=self.attrs.water,
                       muscles=self.attrs.muscles)


class Retriever(AbsRetriever):
    def __init__(self, category: str, uname: str) -> None:
        super().__init__(category, uname)
        self.keiko = Balance


class Balance(Keiko):
    weight = pw.FloatField()
    fat = pw.FloatField(null=True)
    water = pw.FloatField(null=True)
    muscles = pw.FloatField(null=True)


class Umojis(AbsUmojis):
    umoji2uname = {b'\xe2\x9a\x96\xef\xb8\x8f'.decode(): 'balance'}
    emoji2umoji = {b'\xe2\x9a\x96'.decode(): b'\xe2\x9a\x96\xef\xb8\x8f'.decode()}

