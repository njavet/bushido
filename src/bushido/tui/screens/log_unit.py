from typing import Any

from textual.events import Key
from textual.screen import ModalScreen
from textual.suggester import Suggester, SuggestionReady
from textual.widgets import Input

from bushido.core.result import Result
from bushido.modules import ParsedUnit


class LogUnitScreen(ModalScreen[Result[ParsedUnit[Any]]]):
    pass


class UnitSuggester(Suggester):
    def __init__(self, emojis: dict[str, str]) -> None:
        super().__init__()
        self.emojis = emojis

    async def get_suggestion(self, value: str) -> str | None:
        es = [uname for uname, emoji in self.emojis.items() if uname.startswith(value)]
        if len(es) == 1:
            return es[0] + " "
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
