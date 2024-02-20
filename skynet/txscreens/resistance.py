from textual.screen import ModalScreen
from textual.widgets import Collapsible, Label, RichLog

from rich.table import Table


class ResistanceScreen(ModalScreen):
    BINDINGS = [('b', 'app.pop_screen', 'Back')]

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


