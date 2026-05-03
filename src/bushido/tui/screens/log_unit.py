from typing import Any

from rich.console import Group
from rich.panel import Panel
from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import Key
from textual.screen import ModalScreen
from textual.suggester import Suggester, SuggestionReady
from textual.widget import Widget
from textual.widgets import Footer, Input

from bushido.categories import LogUnitService, SessionFactory


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
        super().__init__(suggester=suggester)

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()


class UnitHelpWidget(Widget):
    def __init__(self, log_unit_service: LogUnitService) -> None:
        super().__init__()
        self.log_unit_service = log_unit_service

    def render(self) -> Group:
        panels = []
        for item in self.log_unit_service.category_help:
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


class LogUnitScreen(ModalScreen[Any]):
    BINDINGS = [
        Binding("q", "app.pop_screen", "back"),
    ]

    def __init__(self, log_unit_service: LogUnitService, sf: SessionFactory) -> None:
        super().__init__()
        self.log_unit_service = log_unit_service
        self.sf = sf

    def compose(self) -> ComposeResult:
        yield UnitHelpWidget(self.log_unit_service)
        # yield LogUnitInput(suggester=UnitSuggester(self.log_unit_service.unit_names))
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        with self.sf.session() as session:
            self.log_unit_service.log_unit(event.value, session)
        self.query_one(Input).action_delete_left_all()
        self.query_one(Input).action_delete_right_all()
