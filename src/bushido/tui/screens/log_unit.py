from typing import Awaitable, Callable

from rich.console import Group
from rich.panel import Panel
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Key
from textual.message import Message
from textual.screen import ModalScreen
from textual.suggester import Suggester, SuggestionReady
from textual.widget import Widget
from textual.widgets import Input

from bushido.categories.unit_help import UnitHelpService

LogUnitHandler = Callable[[str], Awaitable[str | None]]


class UnitSuggester(Suggester):
    def __init__(self, unit_names: list[str]) -> None:
        super().__init__()
        self.unit_names = unit_names

    async def get_suggestion(self, value: str) -> str | None:
        names = [name for name in self.unit_names if name.startswith(value)]
        if len(names) == 1:
            return names[0] + " "
        return None


class UnitInput(Input):
    def __init__(self, suggester: UnitSuggester) -> None:
        super().__init__(suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()
            event.stop()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.post_message(UnitSubmitted(event.value.strip()))


class UnitSubmitted(Message):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class UnitHelpWidget(Widget):
    def __init__(self, ch: UnitHelpService) -> None:
        super().__init__()
        self.ch = ch

    def render(self) -> Group:
        panels = []
        for item in self.ch.category_help:
            content = "\n".join(
                [
                    f"Category: {item.name}",
                    f"Grammar: {item.grammar}",
                    f"Units: {', '.join(item.unit_names)}",
                ]
            )
            panel = Panel(
                content,
            )
            panels.append(panel)
        return Group(*panels)


class LogUnitScreen(ModalScreen[bool]):
    def __init__(self, ch: UnitHelpService, log_unit: LogUnitHandler) -> None:
        super().__init__()
        self.ch = ch
        self.log_unit = log_unit

    def compose(self) -> ComposeResult:
        with Vertical():
            yield UnitHelpWidget(self.ch)
            yield UnitInput(suggester=UnitSuggester(self.ch.unit_names))

    async def on_unit_submitted(self, message: UnitSubmitted) -> None:
        if not message.value:
            self.app.notify("empty unit", title="logging failed", severity="error")
            self.dismiss(False)
            return

        error = await self.log_unit(message.value)
        if error:
            self.app.notify(error, title="logging failed", severity="error")
            self.dismiss(False)
        else:
            self.dismiss(True)
