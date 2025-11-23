from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

from bushido.infra.db import SessionFactory


class BushidoApp(App[None]):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("h", "help", "Help"),
        ("m", "manage_units", "Unit"),
    ]
    CSS_PATH = None
    TITLE = "Bushido"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Bushido TUI is running. Press Q to quit.")
        yield Footer()

    def on_mount(self) -> None:
        sf = SessionFactory()
