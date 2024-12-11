from dataclasses import dataclass, field
from sqlalchemy.orm import Session

# project imports
from ulib.db.models import Scale
from ulib.processors import AbsUnitProcessor


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine):
        super().__init__(engine)

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

    def _upload_keiko(self, unit_key):
        scale = Scale(weight=self.attrs.weight,
                      fat=self.attrs.fat,
                      water=self.attrs.water,
                      muscles=self.attrs.muscles,
                      unit=unit_key)
        with Session(self.engine) as session:
            session.add(scale)
            session.commit()

