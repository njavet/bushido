from textual.screen import ModalScreen
from textual.widgets import Pretty


class HelpScreen(ModalScreen):
    BINDINGS = [('q', 'app.pop_screen', 'Back'),
                ('h', 'app.pop_screen', 'Back')]

    def __init__(self, emojis):
        super().__init__()
        self.emojis = emojis

    def compose(self):
        yield Pretty(self.emojis)
