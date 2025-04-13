
# project imports
from bushido.exceptions import ValidationError
from bushido.schema.lifting import KeikoSpec
from bushido.data.categories.lifting import create_keiko_orm


class KeikoProcessor:

    def process_keiko(self, unit_spec):
        keiko_spec = self.parse_keiko(unit_spec.words)
        return create_keiko_orm(keiko_spec)

    @staticmethod
    def parse_keiko(words):
        try:
            weights = [float(w) for w in words[::3]]
            reps = [float(r) for r in words[1::3]]
            pauses = [int(p) for p in words[2::3]] + [0]
        except ValueError:
            raise ValidationError('invalid input')

        if len(reps) != len(weights):
            raise ValidationError(
                'Not the same number of reps and weights')
        if len(pauses) != len(reps):
            raise ValidationError('break error')
        if len(reps) < 1:
            raise ValidationError('No set')

        keiko_spec = KeikoSpec(weights=weights,
                               reps=reps,
                               pauses=pauses)
        return keiko_spec

