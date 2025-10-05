from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static


class BushidoApp(App[None]):
    CSS_PATH = None
    TITLE = "Bushido"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Bushido TUI is running. Press Q to quit.")
        yield Footer()

    def on_mount(self) -> None:
        pass
