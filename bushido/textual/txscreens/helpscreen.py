from textual.screen import ModalScreen
from textual.widgets import Pretty


class HelpScreen(ModalScreen):
    BINDINGS = [('q', 'app.pop_screen', 'Back'),
                ('h', 'app.pop_screen', 'Back')]

    def __init__(self, um):
        super().__init__()
        self.um = um

    def compose(self):
        pass
