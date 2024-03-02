from textual.screen import ModalScreen
from textual.containers import Horizontal
from textual.widgets import Collapsible, Label, RichLog, ProgressBar
import collections
import datetime
from rich.table import Table
from rich.text import Text


class ResistanceScreen(ModalScreen):
    BINDINGS = [('q', 'app.pop_screen', 'Back')]

    def __init__(self, user_id, modname2stats):
        super().__init__()
        self.user_id = user_id
        self.modname2stats = modname2stats

    def compose(self):
        with Collapsible(title='Squat'):
            with Horizontal():
                yield RichLog(id='squat')
                yield ProgressBar(total=1.75, show_eta=False)
        with Collapsible(title='Deadlift'):
            yield RichLog(id='deadlift')
        with Collapsible(title='Benchpress'):
            yield RichLog(id='benchpress')

    def on_mount(self):
        query = self.modname2stats['resistance'].retrieve_units(self.user_id)

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
        self.modname2stats['resistance'].compute_stats(units)
        table = Table('Date', 'Weight', 'Reps', '1RM', 'RS')

        def add_row(unit):
            table.add_row(datetime.datetime.strftime(unit.log_time, '%d.%m.%y'),
                          Text(str(unit.resistanceset.weight)),
                          Text(str(unit.resistanceset.reps)),
                          '{:.0f}'.format(unit.resistanceset.orm),
                          '{:.2f}'.format(unit.resistanceset.rel_strength))

        for s in self.modname2stats['resistance'].heaviest[0:4]:
            add_row(s)
        table.add_section()
        for s in self.modname2stats['resistance'].most_reps[0:4]:
            add_row(s)
        table.add_section()
        for s in self.modname2stats['resistance'].best_orm[0:4]:
            add_row(s)
        table.add_section()
        for s in self.modname2stats['resistance'].best_rs[0:4]:
            add_row(s)

        return table
