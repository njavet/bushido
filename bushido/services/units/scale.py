from dataclasses import dataclass, field
import peewee as pw

# project imports
from bushido.keikolib.abscat import Keiko, AbsProcessor, AbsCategory, AbsUmojis


class Category(AbsCategory):
    def __init__(self, category: str) -> None:
        super().__init__(category)
        self.keiko = Balance


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
