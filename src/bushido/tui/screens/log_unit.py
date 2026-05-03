
from rich.table import Table
from sqlalchemy.orm import Session
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.events import Key
from textual.screen import ModalScreen
from textual.suggester import Suggester, SuggestionReady
from textual.widget import Widget
from textual.widgets import Footer, Input

from bushido.core.result import Err, Warn
from bushido.service.log_unit import LogUnitService, UnitHelp


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


class UnitHelpWidget(Widget):
    def __init__(self, unit_help: dict[str, UnitHelp]) -> None:
        super().__init__()
        self.unit_help = unit_help

    def render(self) -> Table:
        table = Table(
            show_header=False,
            show_edge=False,
            pad_edge=False,
            box=None,
            collapse_padding=True,
        )
        for category, unit_help in self.unit_help.items():
            table.add_row("Category", category)
            table.add_row(unit_help.grammar)
            table.add_row("Units")
            for unit_name in unit_help.unit_names:
                table.add_row(unit_name)
        return table


class LogUnitScreen(ModalScreen[bool]):
    BINDINGS = [
        Binding("q", "app.pop_screen", "back"),
    ]

    def __init__(self, log_unit_service: LogUnitService, session: Session) -> None:
        super().__init__()
        self.log_unit_service = log_unit_service
        self.session = session

    def compose(self) -> ComposeResult:
        yield Grid(
            LogUnitInput(suggester=UnitSuggester(self.log_unit_service.unit_names)),
        )
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> bool:
        result = self.log_unit_service.log_unit(event.value, self.session)
        if isinstance(result, Err):
            return False
        elif isinstance(result, Warn):
            # TODO implement warning
            return False
        else:
            self.query_one(Input).action_delete_left_all()
            self.query_one(Input).action_delete_right_all()
            return True
