from typing import Any

from textual.events import Key
from textual.screen import ModalScreen
from textual.suggester import Suggester, SuggestionReady
from textual.widgets import Input

from bushido.core.result import Result
from bushido.modules import ParsedUnit


class LogUnitScreen(ModalScreen[Result[ParsedUnit[Any]]]):
    BINDINGS = [("q", "app.pop_screen", "back"), ("l", "app.pop_screen", "back")]

    def __init__(self, unit_names: list[str]) -> None:
        super().__init__()
        self.unit_names = unit_names


class UnitSuggester(Suggester):
    def __init__(self, unit_names: list[str]) -> None:
        super().__init__()
        self.unit_names = unit_names

    async def get_suggestion(self, value: str) -> str | None:
        names = [name for name in self.unit_names if name.startswith(value)]
        if len(names) == 1:
            return names[0] + " "
        return None


class TextInput(Input):
    def __init__(self, suggester: UnitSuggester) -> None:
        super().__init__(suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()
