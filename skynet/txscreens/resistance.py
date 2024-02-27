from textual.screen import ModalScreen
from textual.widgets import Collapsible, Label, RichLog
import collections
import datetime
from rich.table import Table
from rich.text import Text


class ResistanceScreen(ModalScreen):
    BINDINGS = [('q', 'app.pop_screen', 'Back')]

    def __init__(self, user_id, units):
        super().__init__()
        self.user_id = user_id
        self.units = units

    def compose(self):
        with Collapsible(title='Big Three'):
            yield Label(Text('Squat', style='bold cyan'))
            yield RichLog(id='squat')
            yield Label(Text('Deadlift', style='bold cyan'))
            yield RichLog(id='deadlift')
            yield Label(Text('Benchpress', style='bold cyan'))
            yield RichLog(id='benchpress')

    def on_mount(self):
        query = self.units['resistance'].unit_retriever.retrieve_units(self.user_id)
        dix = collections.defaultdict(list)
        for unit in query:
            dix[unit.unit_name].append(unit)

        squat = self.get_table(dix['squat'])
        rl = self.query_one('#squat', RichLog)
        rl.write(squat)

        deadlift = self.get_table(dix['deadlift'])
        rl = self.query_one('#deadlift', RichLog)
        rl.write(deadlift)

        benchpress = self.get_table(dix['benchpress'])
        rl = self.query_one('#benchpress', RichLog)
        rl.write(benchpress)

    def get_table(self, units):
        self.units['resistance'].unit_stats.compute_stats(units)

        table = Table('Type', 'Date', 'Weight', 'Reps', '1RM', 'RS')

        def add_row(unit, rectype):
            table.add_row(rectype,
                          datetime.datetime.strftime(unit.log_time, '%d.%m.%y'),
                          Text(str(unit.resistanceset.weight)),
                          Text(str(unit.resistanceset.reps)),
                          '{:.0f}'.format(unit.resistanceset.orm),
                          '{:.2f}'.format(unit.resistanceset.rel_strength))

        add_row(self.units['resistance'].unit_stats.heaviest, 'Heaviest')
        add_row(self.units['resistance'].unit_stats.most_reps, 'Most Reps')
        add_row(self.units['resistance'].unit_stats.best_orm, 'Best 1RM')
        add_row(self.units['resistance'].unit_stats.best_rs, 'Best RS')

        return table
