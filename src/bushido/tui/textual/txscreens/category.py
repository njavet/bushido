from textual.app import ComposeResult
from textual.screen import Screen


class Category(Screen):
    BINDINGS = [("q", "app.pop_screen", "Back")]

    def __init__(self, category):
        super().__init__()
        self.category = category

    def compose(self) -> ComposeResult:
        pass
