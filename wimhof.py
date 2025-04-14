
# project imports
from bushido.exceptions import ValidationError
from bushido.schema.wimhof import KeikoSpec
from bushido.data.categories.wimhof import create_keiko_orm


class KeikoProcessor:

    def process_keiko(self, unit_spec):
        keiko_spec = self.parse_keiko(unit_spec.words)
        return create_keiko_orm(keiko_spec)

    @staticmethod
    def parse_keiko(words):
        try:
            breaths = [float(bs) for bs in words[::2]]
            retentions = [float(r) for r in words[1::2]]
        except ValueError:
            raise ValidationError('invalid input')

        if len(breaths) != len(retentions):
            raise ValidationError(
                'Not the same number of breaths and retentions')
        if len(retentions) < 1:
            raise ValidationError('No round')

        keiko_spec = KeikoSpec(breaths=breaths, retentions=retentions)
        return keiko_spec
