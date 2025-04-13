
# project imports
from bushido.exceptions import ValidationError


class KeikoProcessor:

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

        keiko_spep =
