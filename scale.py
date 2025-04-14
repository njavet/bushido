
# project imports
from bushido.exceptions import ValidationError
from bushido.schema.scale import KeikoSpec
from bushido.data.categories.scale import create_keiko_orm



class KeikoProcessor:

    def process_keiko(self, unit_spec):
        keiko_spec = self.parse_keiko(unit_spec.words)
        return create_keiko_orm(keiko_spec)

    @staticmethod
    def parse_keiko(words):
        try:
            weight = float(words[0])
        except (IndexError, ValueError):
            raise ValidationError('wrong format')

        try:
            belly = float(words[1])
        except ValueError:
            raise ValidationError('wrong belly format')
        except IndexError:
            belly = None

        keiko_spec = KeikoSpec(weight=weight, belly=belly)
        return keiko_spec

