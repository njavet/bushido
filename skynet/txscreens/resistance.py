from textual.screen import ModalScreen
from textual.widgets import Collapsible, Label, RichLog
import datetime
from rich.table import Table
from rich.text import Text

from units import resistance


class ResistanceScreen(ModalScreen):
    BINDINGS = [('q', 'app.pop_screen', 'Back')]

    def __init__(self, user_id, unit_retrievers):
        super().__init__()
        self.user_id = user_id
        self.unit_retrievers = unit_retrievers

    def compose(self):
        rl = Table()
        rl.add_column('Date')
        rl.add_column('Exercise')
        rl.add_column('Weight')
        rl.add_column('Reps')
        rl.add_column('ORM')
        rl.add_column('REl')
        rll = RichLog()
        rll.write(rl)
        for i in range(30):
            with Collapsible():
                yield Label('res' + str(i))
                yield rll


    def render(self):
        exercise = Text(self.heaviest.unit_name.capitalize(), style='bold cyan')

        def get_table(unit, rectype):
            table = Table('Type', 'Date', 'Weight', 'Reps', '1RM', 'RS')
            table.add_row(rectype,
                          datetime.datetime.strftime(unit.log_time, '%d.%m.%y'),
                          Text(str(unit.resistanceset.weight)),
                          Text(str(unit.resistanceset.reps)),
                          '{:.0f}'.format(unit.resistanceset.orm),
                          '{:.2f}'.format(unit.resistanceset.rel_strength))
            return table
        ht = get_table(self.heaviest, 'Heaviest')
        rt = get_table(self.most_reps, 'Most Reps')
        ot = get_table(self.best_orm, 'Best 1RM')
        st = get_table(self.best_rs, 'Best RS')

        return exercise, ht, rt, ot, st
