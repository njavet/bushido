from textual.screen import ModalScreen


class HelpScreen(ModalScreen):
    BINDINGS = [("q", "app.pop_screen", "Back"), ("h", "app.pop_screen", "Back")]

    def __init__(self, um):
        super().__init__()
        self.um = um

    def compose(self):
        pass
