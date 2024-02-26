from textual.screen import ModalScreen
from textual.widgets import Collapsible, Label, RichLog, Static
from textual.containers import Horizontal
import collections
import datetime
from rich.table import Table
from rich.text import Text

from units import resistance


class WimhofScreen(ModalScreen):
    BINDINGS = [('q', 'app.pop_screen', 'Back')]

    def __init__(self, user_id, units):
        super().__init__()
        self.user_id = user_id
        self.units = units

    def compose(self):
        yield Label('Wimhof')
        with Horizontal():
            yield Static('History')
            yield Static('Practice')

    def on_mount(self):
        pass
