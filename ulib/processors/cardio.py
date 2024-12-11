import datetime
from sqlalchemy.orm import Session
from dataclasses import dataclass, field

# project imports
from .abs_unit_proc import AbsUnitProcessor
from ulib.db.models import Cardio
import bushido.parsing as parsing


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    @dataclass
    class Attrs:
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

    def _process_words(self, words: list) -> None:
        # TODO fix this
        # <start_t> <sec> <gym> <distance> <cal> <avghr> <maxhr>
        try:
            start_t = parsing.parse_military_time_string(words[0])
        except IndexError:
            raise ValueError('no start time!')
        except ValueError:
            raise

        try:
            seconds = parsing.parse_time_string(words[1])
        except IndexError:
            raise ValueError('no duration!')
        except ValueError:
            raise

        try:
            gym = words[2]
        except IndexError:
            raise ValueError('no gym!')

        try:
            distance = float(words[3])
        except IndexError:
            distance = None
        except ValueError:
            raise ValueError('CardioUnit: wrong distance format')

        try:
            cal = int(words[4])
        except IndexError:
            cal = None
        except ValueError:
            raise ValueError('CardioUnit: wrong cal format')

        try:
            avghr = int(words[5])
        except IndexError:
            avghr = None
        except ValueError:
            raise ValueError('CardioUnit: wrong avghr format')

        try:
            maxhr = int(words[6])
        except IndexError:
            maxhr = None
        except ValueError:
            raise ValueError('CardioUnit: wrong maxhr format')

        self.attrs = self.Attrs(start_t=start_t,
                                seconds=seconds,
                                gym=gym)
        self.attrs.set_optional_data(distance, cal, avghr, maxhr)

    def _upload_keiko(self, unit_key):
        cardio = Cardio(start_t=self.attrs.start_t,
                        seconds=self.attrs.seconds,
                        gym=self.attrs.gym,
                        distance=self.attrs.distance,
                        cal=self.attrs.cal,
                        avghr=self.attrs.avghr,
                        maxhr=self.attrs.maxhr,
                        unit=unit_key)
        with Session(self.engine) as session:
            session.add(cardio)
            session.commit()

