from dataclasses import dataclass, field
import peewee as pw

# project imports
import unit_processing
import exceptions


class UnitProcessor(unit_processing.UnitProcessor):
    def __init__(self, module_name, unit_name, unit_emoji):
        super().__init__(module_name, unit_name, unit_emoji)

    def parse_words(self, words: list) -> None:
        try:
            self.attrs = Attrs(weight=float(words[0]))
        except (IndexError, ValueError):
            raise exceptions.UnitProcessingError('Specify the weight')

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

    def save_subunit(self):
        self.subunit = Balance.create(unit_id=self.unit,
                                      weight=self.attrs.weight,
                                      fat=self.attrs.fat,
                                      water=self.attrs.water,
                                      muscles=self.attrs.muscles)


@dataclass
class Attrs(unit_processing.Attrs):
    weight: float
    fat: float | None = field(init=False)
    water: float | None = field(init=False)
    muscles: float | None = field(init=False)

    def set_optional_data(self, fat, water, muscles):
        self.fat = fat
        self.water = water
        self.muscles = muscles


class Balance(unit_processing.SubUnit):
    weight = pw.FloatField()
    fat = pw.FloatField(null=True)
    water = pw.FloatField(null=True)
    muscles = pw.FloatField(null=True)
