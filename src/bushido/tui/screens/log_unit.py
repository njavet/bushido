from typing import Any

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import RichLog

from bushido.core.result import Result
from bushido.modules import ParsedUnit
from bushido.tui.widgets.log_unit import LogUnitInput, UnitSuggester


class LogUnitScreen(ModalScreen[Result[ParsedUnit[Any]]]):
    BINDINGS = [("q", "app.pop_screen", "back"), ("l", "app.pop_screen", "back")]

    def __init__(self, unit_names: list[str]) -> None:
        super().__init__()
        self.unit_names = unit_names

    def compose(self) -> ComposeResult:
        yield Grid(
            LogUnitInput(suggester=UnitSuggester(self.unit_names)),
            RichLog(id="log_result"),
        )
