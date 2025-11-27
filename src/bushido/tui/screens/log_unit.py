from typing import Any

from sqlalchemy.orm import Session
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.events import Key
from textual.screen import ModalScreen
from textual.suggester import Suggester, SuggestionReady
from textual.widgets import Input, RichLog

from bushido.core.result import Err, Result, Warn
from bushido.modules import ParsedUnit
from bushido.service.log_unit import LogUnitService


class UnitSuggester(Suggester):
    def __init__(self, unit_names: list[str]) -> None:
        super().__init__()
        self.unit_names = unit_names

    async def get_suggestion(self, value: str) -> str | None:
        names = [name for name in self.unit_names if name.startswith(value)]
        if len(names) == 1:
            return names[0] + " "
        return None


class LogUnitInput(Input):
    def __init__(self, suggester: UnitSuggester) -> None:
        super().__init__(suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()


class LogUnitScreen(ModalScreen[Result[ParsedUnit[Any]]]):
    BINDINGS = [
        Binding("q", "app.pop_screen", "back"),
        Binding("l", "app.pop_screen", "back"),
    ]

    def __init__(self, log_unit_service: LogUnitService, session: Session) -> None:
        super().__init__()
        self.log_unit_service = log_unit_service
        self.session = session

    def compose(self) -> ComposeResult:
        yield Grid(
            LogUnitInput(suggester=UnitSuggester(self.log_unit_service.unit_names)),
            RichLog(id="log_result"),
        )

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        rl = self.query_one("#log_result", RichLog)
        rl.clear()
        result = self.log_unit_service.log_unit(event.value, self.session)
        if isinstance(result, Err):
            rl.write(result.message)
        elif isinstance(result, Warn):
            # TODO implement warning
            pass
        else:
            rl.write("Unit confirmed")
        self.query_one(Input).action_delete_left_all()
        self.query_one(Input).action_delete_right_all()
