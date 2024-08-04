from textual.app import ComposeResult
from textual.screen import Screen


class Lifting(Screen):
    BINDINGS = [('q', 'app.pop_screen', 'Back')]

    def __init__(self, retriever):
        super().__init__()
        self.ret = retriever

    def compose(self) -> ComposeResult:
        pass

