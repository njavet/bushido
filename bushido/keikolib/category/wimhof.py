from dataclasses import dataclass
import peewee as pw

# project imports
from keikolib.abscat import Keiko, AbsProcessor, AbsRetriever, AbsUmojis


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    @dataclass
    class Attrs:
        rounds: list[int]
        breaths: list[int]
        retentions: list[int]

        def zipped(self):
            return zip(self.rounds, self.breaths, self.retentions)

    def _process_words(self, words):
        try:
            breaths = [int(b) for b in words[::2]]
            retentions = [int(r) for r in words[1::2]]
        except ValueError:
            raise ValueError('value error')
        if len(breaths) != len(retentions):
            raise ValueError('Not the same number of breaths and seconds')
        if len(breaths) < 1:
            raise ValueError('At least one round necessary')

        self.attrs = self.Attrs(rounds=list(range(len(breaths))),
                                breaths=breaths,
                                retentions=retentions)

    def _save_keiko(self, unit):
        for round_nr, b, r in self.attrs.zipped():
            Wimhof.create(unit_id=unit,
                          round_nr=round_nr,
                          breaths=b,
                          retention=r)


class Retriever(AbsRetriever):
    def __init__(self, category: str, uname: str) -> None:
        super().__init__(category, uname)
        self.keiko = Wimhof


class Wimhof(Keiko):
    round_nr = pw.IntegerField()
    breaths = pw.IntegerField()
    retention = pw.IntegerField()


class Umojis(AbsUmojis):
    umoji2uname = {
        b'\xf0\x9f\xaa\x90'.decode(): 'wimhof'}

