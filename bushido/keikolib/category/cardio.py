import datetime
import peewee as pw
from dataclasses import dataclass, field

# project imports
from bushido.keiko import Keiko, AbsProcessor, AbsRetriever, AbsAttrs, AbsUmojis
import bushido.parsing as parsing
from bushido.exceptions import ProcessingError


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    def _process_words(self, words: list) -> None:
        # TODO fix this
        # <start_t> <sec> <gym> <distance> <cal> <avghr> <maxhr>
        try:
            start_t = parsing.parse_military_time_string(words[0])
        except IndexError:
            raise ProcessingError('no start time!')
        except ProcessingError:
            raise

        try:
            seconds = parsing.parse_time_string(words[1])
        except IndexError:
            raise ProcessingError('no duration!')
        except ProcessingError:
            raise

        try:
            gym = words[2]
        except IndexError:
            raise ProcessingError('no gym!')

        try:
            distance = float(words[3])
        except IndexError:
            distance = None
        except ValueError:
            raise ProcessingError('CardioUnit: wrong distance format')

        try:
            cal = int(words[4])
        except IndexError:
            cal = None
        except ValueError:
            raise ProcessingError('CardioUnit: wrong cal format')

        try:
            avghr = int(words[5])
        except IndexError:
            avghr = None
        except ValueError:
            raise ProcessingError('CardioUnit: wrong avghr format')

        try:
            maxhr = int(words[6])
        except IndexError:
            maxhr = None
        except ValueError:
            raise ProcessingError('CardioUnit: wrong maxhr format')

        self.attrs = Attrs(start_t=start_t,
                           seconds=seconds,
                           gym=gym)
        self.attrs.set_optional_data(distance, cal, avghr, maxhr)

    def _save_keiko(self, unit):
        Cardio.create(unit_id=unit,
                      start_t=self.attrs.start_t,
                      seconds=self.attrs.seconds,
                      gym=self.attrs.gym,
                      distance=self.attrs.distance,
                      cal=self.attrs.cal,
                      avghr=self.attrs.avghr,
                      maxhr=self.attrs.maxhr)


@dataclass
class Attrs(AbsAttrs):
    start_t: datetime.time
    seconds: float
    gym: str
    distance: float | None = field(init=False)
    cal: int | None = field(init=False)
    avghr: int | None = field(init=False)
    maxhr: int | None = field(init=False)

    def set_optional_data(self, distance, cal, avghr, maxhr):
        self.distance = distance
        self.cal = cal
        self.avghr = avghr
        self.maxhr = maxhr


class Cardio(Keiko):
    # TODO switch to unix utc timestamps
    start_t = pw.TimeField()
    seconds = pw.FloatField()
    gym = pw.CharField()
    distance = pw.FloatField(null=True)
    cal = pw.IntegerField(null=True)
    avghr = pw.IntegerField(null=True)
    maxhr = pw.IntegerField(null=True)

    def seconds2time_str(self):
        m, s = divmod(int(self.seconds), 60)
        return str(m).zfill(2) + ':' + str(s).zfill(2)

    def __str__(self):
        return ', '.join([self.seconds2time_str(),
                          str(self.distance),
                          '{:0.1f}'.format(self.avg_speed),
                          str(self.avghr),
                          str(self.maxhr),
                          str(self.cal)])


class Umojis(AbsUmojis):
    umoji2uname = {
           b'\xf0\x9f\xaa\x96'.decode(): 'running',
           b'\xf0\x9f\xa6\x88'.decode(): 'swimming'}
