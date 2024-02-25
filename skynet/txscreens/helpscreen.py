# general import*s
from textual.screen import ModalScreen
from textual.widgets import Pretty

import config


class HelpScreen(ModalScreen):
    BINDINGS = [('q', 'app.pop_screen', 'Back')]

    def __init__(self):
        super().__init__()

    def compose(self):
        yield Pretty(config.emojis)

