from typing import Any

from textual.screen import ModalScreen


class HelpScreen(ModalScreen[Any]):
    BINDINGS = [("q", "app.pop_screen", "Back"), ("h", "app.pop_screen", "Back")]
